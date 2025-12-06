module top (
    input  wire sys_clk,      // 27 MHz
    input  wire sys_rst_n,
    input  wire trigger_in,   // (Ignorado, usamos auto-trigger)
    input  wire [7:0] adc_data,
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

    // --- GENERADOR SENOIDAL (LUT 64 Puntos) ---
    reg [7:0] sine_rom [0:63];
    reg [5:0] rom_addr;
    
    // Inicialización de la onda (Offset 128, Amplitud +/- 127)
    initial begin
        sine_rom[0] = 128; sine_rom[1] = 140; sine_rom[2] = 153; sine_rom[3] = 165; 
        sine_rom[4] = 177; sine_rom[5] = 188; sine_rom[6] = 199; sine_rom[7] = 209; 
        sine_rom[8] = 219; sine_rom[9] = 227; sine_rom[10] = 235; sine_rom[11] = 241; 
        sine_rom[12] = 247; sine_rom[13] = 251; sine_rom[14] = 254; sine_rom[15] = 255; 
        sine_rom[16] = 255; sine_rom[17] = 254; sine_rom[18] = 251; sine_rom[19] = 247; 
        sine_rom[20] = 241; sine_rom[21] = 235; sine_rom[22] = 227; sine_rom[23] = 219; 
        sine_rom[24] = 209; sine_rom[25] = 199; sine_rom[26] = 188; sine_rom[27] = 177; 
        sine_rom[28] = 165; sine_rom[29] = 153; sine_rom[30] = 140; sine_rom[31] = 128; 
        sine_rom[32] = 115; sine_rom[33] = 103; sine_rom[34] = 90; sine_rom[35] = 78; 
        sine_rom[36] = 67; sine_rom[37] = 56; sine_rom[38] = 46; sine_rom[39] = 36; 
        sine_rom[40] = 28; sine_rom[41] = 20; sine_rom[42] = 14; sine_rom[43] = 8; 
        sine_rom[44] = 4; sine_rom[45] = 1; sine_rom[46] = 0; sine_rom[47] = 0; 
        sine_rom[48] = 1; sine_rom[49] = 4; sine_rom[50] = 8; sine_rom[51] = 14; 
        sine_rom[52] = 20; sine_rom[53] = 28; sine_rom[54] = 36; sine_rom[55] = 46; 
        sine_rom[56] = 56; sine_rom[57] = 67; sine_rom[58] = 78; sine_rom[59] = 90; 
        sine_rom[60] = 103; sine_rom[61] = 115; sine_rom[62] = 127; sine_rom[63] = 128;
    end

    // Incremento continuo de la fase (Frecuencia = 27MHz / 64 ≈ 421 kHz)
    always @(posedge sys_clk) begin
        rom_addr <= rom_addr + 1;
    end

    // --- AUTO-TRIGGER (Simulación de PRF 2kHz) ---
    reg [13:0] trig_cnt; 
    wire auto_trigger = (trig_cnt == 0); // Disparo periódico
    always @(posedge sys_clk) trig_cnt <= trig_cnt + 1;

    // --- ESCRITURA EN MEMORIA ---
    always @(posedge sys_clk) begin
        if (ram_write_en) begin
            memory[ptr] <= sine_rom[rom_addr]; // Guardamos la onda senoidal
        end
        mem_read_data <= memory[ptr]; 
    end

    // --- MÁQUINA DE ESTADOS (Idéntica a la anterior) ---
    localparam IDLE = 0, CAPTURE = 1, SENDING = 2;
    reg [1:0] state = IDLE;
    reg tx_start = 0;
    reg [7:0] tx_byte_latch;
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
                        if (ptr == BURST_SIZE) state <= IDLE;
                        else begin
                            tx_byte_latch <= mem_read_data; 
                            tx_start <= 1;
                            ptr <= ptr + 1;
                        end
                    end else tx_start <= 0;
                end
            endcase
        end
    end

    uart_tx_module uart_inst (
        .clk(sys_clk), .rst_n(sys_rst_n), .tx_start(tx_start),
        .tx_data(tx_byte_latch), .uart_tx(uart_tx), .tx_busy(tx_busy)
    );
endmodule