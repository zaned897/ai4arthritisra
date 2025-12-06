module top (
    input  wire sys_clk,      // 27 MHz Clock
    input  wire sys_rst_n,    // Reset (Botón S1)
    input  wire trigger_in,   // Señal de Trigger del Láser (5kHz)
    input  wire [7:0] adc_data, // Datos reales del AD9226
    output wire adc_clk,      // Reloj hacia ADC
    output wire uart_tx,      // TX hacia PC
    output wire led_busy      // LED indicador
);

    parameter BURST_SIZE = 1024;

    assign adc_clk = ~sys_clk;

    (* ram_style = "block" *)
    reg [7:0] memory [0:BURST_SIZE-1];
    reg [7:0] mem_read_data;
    reg [10:0] ptr; 
    reg ram_write_en;

    always @(posedge sys_clk) begin
        if (ram_write_en) begin
            //memory[ptr] <= adc_data; // Enable this line to use real ADC data
            memory[ptr] <= ptr[7:0];
        end
        mem_read_data <= memory[ptr]; 
    end

    localparam IDLE = 0, CAPTURE = 1, SENDING = 2;
    reg [1:0] state = IDLE;

    reg trig_d1, trig_d2;
    wire trigger_posedge = (trig_d1 && !trig_d2);

    always @(posedge sys_clk) begin
        trig_d1 <= trigger_in;
        trig_d2 <= trig_d1;
    end

    // Lógica UART
    reg tx_start = 0;
    reg [7:0] tx_byte_latch; // Buffer temporal para transmisión
    wire tx_busy;
    assign led_busy = (state == IDLE);

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
                    if (trigger_posedge) state <= CAPTURE;
                end

                CAPTURE: begin
                    // Activamos escritura
                    ram_write_en <= 1; 
                    
                    // Control del puntero
                    if (ptr == BURST_SIZE - 1) begin
                        ptr <= 0;
                        ram_write_en <= 0; // Dejar de escribir al terminar
                        state <= SENDING;
                    end else begin
                        ptr <= ptr + 1;
                    end
                end

                SENDING: begin
                    ram_write_en <= 0; // Asegurar que no escribimos
                    
                    if (!tx_busy && !tx_start) begin
                        if (ptr == BURST_SIZE) begin
                            state <= IDLE;
                        end else begin
                            // Leemos el dato que sale del bloque RAM
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