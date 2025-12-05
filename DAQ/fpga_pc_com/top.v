module top(
    input  sys_clk,
    input  sys_rst_n,
    output uart_tx,
    output [5:0] led
);

    parameter BURST_SIZE = 64;
    
    localparam IDLE    = 0;
    localparam CAPTURE = 1;
    localparam SENDING = 2;

    reg [1:0] state = IDLE;
    reg [7:0] memory [0:BURST_SIZE-1];
    reg [5:0] ptr = 0;
    
    reg tx_start = 0;
    reg [7:0] tx_data = 0;
    wire tx_busy;

    assign led = ~state;

    uart_tx #(
        .CLK_FREQ(27000000), 
        .BAUD_RATE(115200)
    ) uart_inst (
        .clk(sys_clk),
        .rst_n(sys_rst_n),
        .tx_start(tx_start),
        .tx_data(tx_data),
        .tx_busy(tx_busy),
        .uart_tx(uart_tx)
    );

    always @(posedge sys_clk or negedge sys_rst_n) begin
        if (!sys_rst_n) begin
            state <= IDLE;
            ptr <= 0;
            tx_start <= 0;
        end else begin
            case (state)
            
                IDLE: begin
                    ptr <= 0;
                    state <= CAPTURE; 
                end

                CAPTURE: begin
                    memory[ptr] <= ptr[7:0]; 

                    if (ptr == BURST_SIZE - 1) begin
                        ptr <= 0;
                        state <= SENDING;
                    end else begin
                        ptr <= ptr + 1;
                    end
                end

                SENDING: begin
                    if (!tx_busy && !tx_start) begin
                        tx_data <= memory[ptr];
                        tx_start <= 1;
                    end else if (tx_start) begin
                        tx_start <= 0;
                    end else if (!tx_busy && ptr < BURST_SIZE) begin 
                        ptr <= ptr + 1;
                        
                        if (ptr == BURST_SIZE - 1) begin
                            state <= CAPTURE;
                        end
                    end
                end
            endcase
        end
    end
endmodule
