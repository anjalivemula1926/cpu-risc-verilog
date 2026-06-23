`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 22.06.2026 16:46:13
// Design Name: 
// Module Name: tb_cpu
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module tb_cpu();

    reg        clk;
    reg        rst;
    wire [7:0] reg_wr_data;
    wire [2:0] reg_wr_addr;
    wire       reg_wr_en;
    wire [7:0] alu_result;
    wire       zero;
    wire       carry;
    wire [5:0] pc;
    wire [15:0] instruction;
    wire [7:0] debug_r0;
    wire [7:0] debug_r1;
    wire [7:0] debug_r2;
    wire [7:0] debug_r3;
    wire [7:0] debug_r4;
    wire [7:0] debug_r5;
    wire [7:0] debug_r6;
    wire [7:0] debug_r7;

    cpu_connect dut (
        .clk         (clk),
        .rst         (rst),
        .reg_wr_data (reg_wr_data),
        .reg_wr_addr (reg_wr_addr),
        .reg_wr_en   (reg_wr_en),
        .alu_result  (alu_result),
        .zero        (zero),
        .carry       (carry),
        .pc          (pc),
        .instruction (instruction),
        .debug_r0    (debug_r0),
        .debug_r1    (debug_r1),
        .debug_r2    (debug_r2),
        .debug_r3    (debug_r3),
        .debug_r4    (debug_r4),
        .debug_r5    (debug_r5),
        .debug_r6    (debug_r6),
        .debug_r7    (debug_r7)
    );

    initial clk = 0;
    always #50 clk = ~clk;

    initial begin
        rst = 1;
        repeat(5) @(posedge clk); #1;
        rst = 0;

        // cycle 1 - MOV R0, 5
        @(posedge clk); #1;
        if (debug_r0 == 8'd5)
            $display("PASS - MOV R0,5  → R0 = %0d", debug_r0);
        else
            $display("FAIL - MOV R0,5  → R0 = %0d expected 5", debug_r0);

        // cycle 2 - MOV R1, 3
        @(posedge clk); #1;
        if (debug_r1 == 8'd3)
            $display("PASS - MOV R1,3  → R1 = %0d", debug_r1);
        else
            $display("FAIL - MOV R1,3  → R1 = %0d expected 3", debug_r1);

        // cycle 3 - ADD R2 = R0 + R1 = 8
        @(posedge clk); #1;
        if (debug_r2 == 8'd8)
            $display("PASS - ADD R2    → R2 = %0d", debug_r2);
        else
            $display("FAIL - ADD R2    → R2 = %0d expected 8", debug_r2);

        // cycle 4 - SUB R2 = R2 - R1 = 5
        @(posedge clk); #1;
        if (debug_r2 == 8'd5)
            $display("PASS - SUB R2    → R2 = %0d", debug_r2);
        else
            $display("FAIL - SUB R2    → R2 = %0d expected 5", debug_r2);

        // print all register values at end
        $display("─────────────────────────────");
        $display("Final register state:");
        $display("R0 = %0d", debug_r0);
        $display("R1 = %0d", debug_r1);
        $display("R2 = %0d", debug_r2);
        $display("R3 = %0d", debug_r3);
        $display("R4 = %0d", debug_r4);
        $display("R5 = %0d", debug_r5);
        $display("R6 = %0d", debug_r6);
        $display("R7 = %0d", debug_r7);
        $display("─────────────────────────────");

        repeat(5) @(posedge clk);
        $finish;
    end

endmodule
