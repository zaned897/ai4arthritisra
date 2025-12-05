module top(
    input  sys_clk,      // 27 MHz Clock
    input  sys_rst_n,    // Botón Reset/Trigger (Activo bajo)
    output uart_tx,      // Salida de datos al PC
    output [5:0] led     // LEDs de estado
);

    // --- PARÁMETROS DE CONFIGURACIÓN ---
    parameter BURST_SIZE = 64; // Tamaño del buffer (0 a 63)
    
    // --- MÁQUINA DE ESTADOS (FSM) ---
    localparam IDLE    = 0;
    localparam CAPTURE = 1;
    localparam SENDING = 2;

    // --- REGISTROS Y VARIABLES ---
    reg [1:0] state = IDLE;
    
    // RAM interna (Implementada con DFFs en este caso)
    reg [7:0] memory [0:BURST_SIZE-1]; 
    
    // Puntero de 6 bits (Suficiente para contar de 0 a 63)
    reg [5:0] ptr = 0;
    
    // Señales para control UART
    reg tx_start = 0;
    reg [7:0] tx_data = 0;
    wire tx_busy;

    // Asignación de LEDs (Visualización del estado actual)
    assign led = ~state;

    // --- INSTANCIA DEL MÓDULO UART_TX ---
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

    // --- LÓGICA SECUENCIAL PRINCIPAL (FSM) ---
    always @(posedge sys_clk or negedge sys_rst_n) begin
        if (!sys_rst_n) begin
            // Reset asíncrono
            state <= IDLE;
            ptr <= 0;
            tx_start <= 0;
        end else begin
            case (state)
            
                IDLE: begin
                    // Al soltar el reset (sys_rst_n=1), iniciamos el proceso.
                    ptr <= 0;
                    state <= CAPTURE; 
                end

                CAPTURE: begin
                    // Generación del patrón de Diente de Sierra (0, 1, 2... 63)
                    memory[ptr] <= ptr[7:0]; 

                    if (ptr == BURST_SIZE - 1) begin
                        // Al terminar de escribir el último dato (63)
                        ptr <= 0;
                        state <= SENDING;
                    end else begin
                        ptr <= ptr + 1;
                    end
                end

                SENDING: begin
                    if (!tx_busy && !tx_start) begin
                        // 1. Cargar el dato actual y enviar pulso de inicio
                        tx_data <= memory[ptr];
                        tx_start <= 1;
                        
                        // 2. AVANZAR el puntero al próximo dato (Look-ahead)
                        if (ptr == BURST_SIZE - 1) begin
                            ptr <= 0; // Se envió el dato 63, el próximo dato a leer es el 0
                        end else begin
                            ptr <= ptr + 1;
                        end
                        
                    end else if (tx_start) begin
                        // 3. Desactivar el pulso de inicio
                        tx_start <= 0;

                        // 4. Comprobar si se terminó la ráfaga (ptr se reinició a 0 en el paso anterior)
                        if (ptr == 0) begin 
                            state <= CAPTURE; // Bucle continuo: Volver a generar/enviar
                        end

                    end
                end
                
                // Opción por defecto (manejo de estados inválidos)
                default: state <= IDLE;
                
            endcase
        end
    end
endmodule
