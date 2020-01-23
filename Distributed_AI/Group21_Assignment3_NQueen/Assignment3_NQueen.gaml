/**
* Name: Assignment3
* Author: Khushdeep Singh
* Description: 
* Tags: Tag1, Tag2, TagN
*/

model Assignment3

/* Insert your model definition here */

global {
	geometry bounds <- rectangle ( {0,0}, {200,200});
	
	int N <- 8;	
	
	init
		{    		
	          list<list<rgb>> color_list <- [];
			  loop k from: 1 to: N 
				 {
					list<rgb> colour <- [];			
					loop l from: 1 to: N
					{  colour << (((k + l) mod 2) = 0) ? #yellow : #brown;  }
					color_list << colour;		
				}
				
			 list<rgb> colour <- []; 
				loop i from: 1 to: N
						{	colour<< #yellow;	}
			 color_list << colour;
			
			 ask Chesscell 
					{ color <- color_list[grid_y][grid_x]; } 
	     		 
	    }	
}

grid Chesscell width: N height: N neighbors: 4 { }
   
species queen skills: [fipa,moving]
{   int index;

	list<int> used_Diag1;
	list<int> used_Diag2;
	list<int> used_Rows;
	list<int> ok_positions;
	
	
	message request;
	bool hasRequest;
	
	queen previous;
	

	reflex On_receving_position when: length(informs) > 0 {
		
		message inform <- informs[0];
		write ' receivers message is ' + inform;
		
		used_Rows <- inform.contents[0];
		used_Diag1 <- inform.contents[1];
		used_Diag2 <- inform.contents[2];
		loop r over: 0 to (N - 1) {
			if !(used_Rows contains r) and !(used_Diag1 contains (r - index)) and !(used_Diag2 contains (r + index)) {
				ok_positions <- ok_positions + r;
				write ' receivers ok_position is ' + ok_positions;
			}
		}
		
		if length(ok_positions) = 0 {
			do start_conversation to: [previous] protocol: 'fipa-request' performative: 'request' contents: ['newPositions'];
		    write ' ok-position is zero';
		} 
		else if hasRequest {
			do inform message: request contents: [used_Rows + ok_positions[0], used_Diag1 + (ok_positions[0] - index), used_Diag2 + (ok_positions[0] + index)];
			hasRequest <- false;
			write ' had an request ';
		}
	}
	
	reflex goToPosition when: length(ok_positions) > 0 {
		
		  location<- Chesscell[ok_positions[0]+ N*index];  // N*ok_positions[0]+ index
		  write ' going to target position ' + ok_positions[0];
	}
	
	reflex On_receiving_request when: length(requests) > 0 {
		write ' ok-positions contains '+ ok_positions;
		request <- requests[0];
		if request.contents[0] = 'positions' {
			do agree message: request contents: [];
			write ' 1. agree request message is ' + request;
			
			do inform message: request contents: [used_Rows + ok_positions[0], used_Diag1 + (ok_positions[0] - index), used_Diag2 + (ok_positions[0] + index)];
			write ' 1. inform request message contains ' + request;
		}
		
		else if request.contents[0] = 'newPositions' {
			do agree message: request contents: [];
			write ' Give an new position now ';
			write ' 2. agree request message is '+ request ;
			
			ok_positions <- ok_positions - ok_positions[0];
			write ' Now ok-positions become ' + ok_positions;
			
				if length(ok_positions) > 0 {
					do inform message: request contents: [used_Rows + ok_positions[0], used_Diag1 + (ok_positions[0] - index), used_Diag2 + (ok_positions[0] + index)];	
				    write ' 2. inform request message is ' + request ;
				} 
				else {
					hasRequest <- true;
					do start_conversation to: [previous] protocol: 'fipa-request' performative: 'request' contents: ['newPositions'];
				    write ' 3. New conversation started is ' + request;
				}
		}
	}
	    
	aspect default{
		draw circle(4) at: location color: #blue;
		}
}


experiment assignment3_nqueens type: gui{
	 
	list<queen> nqueens;
	
	init 
	{ create queen returns: q   
		{
			index<- 0;
			ok_positions<- 0 to (N-1);
			write ' Allowed positions are  '+ ok_positions;

			location<- Chesscell[N*index ];
			
			write ' index is ' + index;
		}
		nqueens<- q;
		write ' queen list is ' + nqueens;
	} 
	
	reflex CreateQueen when: length(nqueens)< N and length(last(nqueens).ok_positions) >0
	 {  create queen returns: q
	 	{   index<- length(myself.nqueens);
	 		write' Queen creation no. '+ index;
	    
	        previous<- last(myself.nqueens);
	        write ' previous queen was ' + previous;
	        
	        location<-Chesscell[N*index ];    //index
	 		do start_conversation to: [previous] protocol: 'fipa-request' performative: 'request' contents: ['positions'];
	    }	
	    
	    nqueens<- nqueens + q;
	    write ' new queen added is '+ q;
	    write 'So now nqueens list contains ' + nqueens;
	 }

	output{
		display map type: opengl{
			grid Chesscell lines: #black;
			species queen;
		}
	}	
}

	