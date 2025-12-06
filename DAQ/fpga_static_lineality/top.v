module top (
    input  wire sys_clk,      // 27 MHz Clock
    input  wire sys_rst_n,    // Reset (Botón S1 - Solo para reiniciar todo al principio)
    input  wire trigger_in,   // (IGNORADO: Usamos auto-trigger)
    input  wire [7:0] adc_data, // (IGNORADO)
    output wire adc_clk,      
    output wire uart_tx,      
    output wire led_busy      
);

    parameter BURST_SIZE = 1024;
    assign adc_clk = ~sys_clk;

    (* ram_style = "block" *)
    reg [7:0] memory [0:BURST_SIZE-1];
    reg [7:0] mem_read_data;
    reg [10:0] ptr; 
    reg ram_write_en;

    // --- 1. GENERADOR DE VOLTAJE VIRTUAL (Rampa lenta 0-255) ---
    reg [23:0] slow_cnt;   
    reg [7:0] virtual_voltage; 

    always @(posedge sys_clk or negedge sys_rst_n) begin
        if (!sys_rst_n) begin
            slow_cnt <= 0;
            virtual_voltage <= 0;
        end else begin
            slow_cnt <= slow_cnt + 1;
            // Velocidad: Incrementa 1 LSB cada ~0.3 segundos
            if (slow_cnt == 8000000) begin 
                slow_cnt <= 0;
                virtual_voltage <= virtual_voltage + 1;
            end
        end
    end

    // --- 2. AUTO-TRIGGER (Disparo rápido interno) ---
    // Generamos un pulso cada ~200us para enviar datos constantemente
    reg [12:0] trig_cnt;
    wire auto_trigger = (trig_cnt == 0);
    
    always @(posedge sys_clk) begin
        trig_cnt <= trig_cnt + 1; // Contador libre
    end

    // --- ESCRITURA EN MEMORIA ---
    always @(posedge sys_clk) begin
        if (ram_write_en) begin
            memory[ptr] <= virtual_voltage; 
        end
        mem_read_data <= memory[ptr]; 
    end

    // --- MÁQUINA DE ESTADOS ---
    localparam IDLE = 0, CAPTURE = 1, SENDING = 2;
    reg [1:0] state = IDLE;

    // Lógica UART
    reg tx_start = 0;
    reg [7:0] tx_byte_latch;
    wire tx_busy;
    assign led_busy = (state == IDLE); // LED parpadea rápido

    always @(posedge sys_clk or negedge sys_rst_n) begin
        if (!sys_rst_n) begin
            state <= IDLE;
            ptr <= 0;
            tx_start <= 0;
            ram_write_en <= 0;
        end else begin
            case (state)
                IDLE: begin
                    ptr <= 0;
                    ram_write_en <= 0;
                    // Usamos auto_trigger en lugar del botón externo
                    if (auto_trigger) state <= CAPTURE;
                end

                CAPTURE: begin
                    ram_write_en <= 1; 
                    if (ptr == BURST_SIZE - 1) begin
                        ptr <= 0;
                        ram_write_en <= 0;
                        state <= SENDING;
                    end else begin
                        ptr <= ptr + 1;
                    end
                end

                SENDING: begin
                    ram_write_en <= 0;
                    if (!tx_busy && !tx_start) begin
                        if (ptr == BURST_SIZE) begin
                            state <= IDLE;
                        end else begin
                            tx_byte_latch <= mem_read_data; 
                            tx_start <= 1;
                            ptr <= ptr + 1;
                        end
                    end else begin
                        tx_start <= 0;
                    end
                end
            endcase
        end
    end

    uart_tx_module uart_inst (
        .clk(sys_clk),
        .rst_n(sys_rst_n),
        .tx_start(tx_start),
        .tx_data(tx_byte_latch),
        .uart_tx(uart_tx),
        .tx_busy(tx_busy)
    );

endmodule
