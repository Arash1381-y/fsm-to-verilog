module moore_fsm #(parameter N_STATE=4)(input clk, input reset, input in, output reg out);

reg [1:0] state, next_state;

always @(posedge clk) begin
		 if (reset) begin
			state <= 0;
		end else begin
			state <= next_state;
		end
	
end

always @(in or state) begin
		case (state)
			2'b00: begin
				 if (in == 1'b1) begin
					next_state = 2'b01;
				end else if (in == 1'b0) begin
					next_state = 2'b00;
				end 
			end
			2'b01: begin
				 if (in == 1'b1) begin
					next_state = 2'b10;
				end else if (in == 1'b0) begin
					next_state = 2'b00;
				end 
			end
			2'b10: begin
				 if (in == 1'b0) begin
					next_state = 2'b11;
				end else if (in == 1'b1) begin
					next_state = 2'b10;
				end 
			end
			2'b11: begin
				 if (in == 1'b1) begin
					next_state = 2'b01;
				end else if (in == 1'b0) begin
					next_state = 2'b11;
				end 
			end
		endcase
	
end

always @(state) begin
		 if (state==2'b00) begin
			out = 1'b0;
		end else if (state==2'b01) begin
			out = 1'b0;
		end else if (state==2'b10) begin
			out = 1'b0;
		end else if (state==2'b11) begin
			out = 1'b1;
		end 
end
endmodule