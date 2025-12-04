module top (
    input wire clk,
    input wire [3:0] adc_data,
    output reg adc_clk,
    output reg uart_tx,
    output wire led_test
);

    reg [1:0] clk_div;
    always @(posedge clk) begin
        clk_div <= clk_div + 1;
        adc_clk <= clk_div[1];
    end

    parameter CLK_FREQ = 27000000;
    parameter BAUD_RATE = 115200;
    parameter CLK_PER_BIT = CLK_FREQ / BAUD_RATE;

    reg [13:0] baud_cnt = 0;
    reg [2:0] bit_idx = 0;
    reg [7:0] tx_byte = 0;
    reg tx_busy = 0;
    reg [3:0] state = 0;

    reg [23:0] send_timer = 0;
    reg start_tx = 0;

    always @(posedge clk) begin
        if (send_timer < 2700000) begin
            send_timer <= send_timer + 1;
            start_tx <= 0;
        end else begin
            send_timer <= 0;
            tx_byte <= {4'b0000, adc_data};
            start_tx <= 1;
        end

        case (state)
            0: begin
                uart_tx <= 1;
                if (start_tx && !tx_busy) begin
                    tx_busy <= 1;
                    state <= 1;
                    baud_cnt <= 0;
                end
            end
            1: begin
                uart_tx <= 0;
                if (baud_cnt < CLK_PER_BIT-1) baud_cnt <= baud_cnt + 1;
                else begin
                    baud_cnt <= 0;
                    state <= 2;
                    bit_idx <= 0;
                end
            end
            2: begin
                uart_tx <= tx_byte[bit_idx];
                if (baud_cnt < CLK_PER_BIT-1) baud_cnt <= baud_cnt + 1;
                else begin
                    baud_cnt <= 0;
                    if (bit_idx < 7) bit_idx <= bit_idx + 1;
                    else state <= 3;
                end
            end
            3: begin
                uart_tx <= 1;
                if (baud_cnt < CLK_PER_BIT-1) baud_cnt <= baud_cnt + 1;
                else begin
                    state <= 0;
                    tx_busy <= 0;
                end
            end
        endcase
    end

    assign led_test = ~uart_tx;

endmodule
