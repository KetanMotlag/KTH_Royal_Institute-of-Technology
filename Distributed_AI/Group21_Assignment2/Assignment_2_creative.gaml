/**
* Name: Assignment2
* Author: Khushdeep Singh
* Description: 
* Tags: Tag1, Tag2, TagN
*/

model Assignment2

/* Insert your model definition here */

global {
	geometry bounds <- rectangle ( {0,0}, {200,200});
	
	int cd_price<- 750;
	int number_of_buyers<- 5;
	int i <-0;
	int j <- 0;
	int k<- 0;
	
	int shoe_buyers <- 0;
	int highest_value<- 0;
	list<int> highest<- [1,2,3,4,5,6,7,8,9,10,11,12];
	
	point japanese_selling_position<- { 80,20};
	point leaving_place<- { 100,0};
	
	bool No_selling_japanese<- false; 
	bool japanese_auction_ended<- true;
	
	bool reached_japanese_auction<- false; 
    bool japanese_participant_move<- false;
    
    bool start_japanese_auction<- true;
 
	init {	
		create Participant number: number_of_buyers { location<- {rnd(100),rnd(100)} ; }
		create japanese_Initiator number: 1   { write 'Japanese Auction begins'; 
			write 'shoe price initially is: ' + cd_price; 
			location<- flip(0.5) ? {55 + rnd(10), 30 + rnd(10)} : { 10+ rnd(10), 55+ rnd(10)};
		}
		create selling_place number: 1      {  }
 	   }
	}




species japanese_Initiator skills: [fipa,moving]{
	list<Participant> part;
	
	point target_point<- nil;	
    bool motion <- true;
				
	reflex movement when: motion and start_japanese_auction
		{	target_point<- japanese_selling_position;
			japanese_auction_ended<- false;
			do goto target:target_point speed: 2.0 ;	
			if(location distance_to(target_point ) < 3){
	 				 motion<- false;  
	 				 japanese_participant_move<- true; 
	 			 }
		}
		
	reflex send_request when: !motion and !japanese_auction_ended and reached_japanese_auction {
		part<- Participant ;	
		
		do start_conversation to: part protocol: 'fipa-contract-net' performative: 'cfp' contents: ['go sleeping'];
		write 'shoe price finally is '+ cd_price;}
		
	reflex read_agree_message when: !(empty(proposes)) and !japanese_auction_ended {
		No_selling_japanese <- true;	
		japanese_auction_ended<- true;
		loop a over: proposes{
			write 'agree message with content: ' + string(a.contents);
	 	    }  
	    }
	    
	reflex read_failure_message when: !(empty(refuses)) and empty(proposes) and !japanese_auction_ended 
		{	 write ' You do not enough money for japanese Auction';
             write ' japanese Auction has been cancelled now!! ';  
             No_selling_japanese<- true;
			 japanese_auction_ended<- true; 
          }
     reflex goto_die when: No_selling_japanese and japanese_auction_ended
     	{ 
			target_point<- leaving_place;
			do goto target: target_point speed: 3.0;
			if ( location distance_to(target_point)<3)
				  	{ do die;    }
	    }      
	
	aspect default{
		draw ellipse(5,8) at: location color: #brown;
	}
}
species Participant skills: [moving,fipa] {
	
	point target_point<- nil;
	bool motion<- true;
	rgb mycolor<- #red;
	int my_price_dutch ;
	int my_price_japanese;
	int b<- rnd(2,3);
	bool random_movement<- true ;
	bool count<- true; 
	  
	reflex count_people when: count
	{  if(  shoe_buyers != number_of_buyers)
		 {if (b=3)
			{ shoe_buyers<- shoe_buyers + 1 ;	 }	
		}
		
		else if (  shoe_buyers = number_of_buyers) 
		     {   	count<- false;  }
	}
	
     
	reflex goto_cd_seller when: motion and (b=3) and japanese_participant_move
	{		my_price_japanese<- rnd(600,900);			
			mycolor<- #green;
		    target_point<- japanese_selling_position;
		    do goto target:target_point speed: 4.0; 
		    if(location distance_to(target_point ) < 3){
	 			motion<- false;
	 			write 'japanese ' + ( j+1) +  ' referred price is: ' + my_price_japanese;
	 	  			  if (j != shoe_buyers+ 1)
	 			  		 {  
	 			  		 	highest[j+1]<- my_price_japanese ;	 
	 			  		 		  		 	
	 			  		 	if ( highest[j+1]> highest_value) 
	 			  		 	{ highest_value<- highest[j+1]; 
	 			  		 	 	 if ( cd_price> highest_value)
	 			  		 	 		 {  write ' you cannot buy shoe , next one please';
	 			  		 	 		 	cd_price<- cd_price + 10;
	 			  		 	 		 	write 'Now shoe_price is : '+ cd_price;
	 			  		 			  }	
	 			  		 	  
	 			  		 	 	 else if ( cd_price< highest_value)
	 			  		 	 		 { write 'OK you can buy shoe at this price ';
	 			  		 	 		 	cd_price<- highest_value;
	 			  		 	 		 	reached_japanese_auction<- true;
	 			  		 	 		 	japanese_participant_move<- false;
	 			  		 			  }
	 			  		 			 }    
	 			  		 	} 
       					j<- j+1;	
       			if( j= shoe_buyers -1 )
	 			  		{write 'Japanese auction is a failure'; } }	         	   
	 	}         
	
	reflex success_japanese_message when: !(empty(cfps)) and !motion and !japanese_auction_ended and (my_price_japanese >= cd_price) and reached_japanese_auction
	 {
		japanese_auction_ended<- true; 
		No_selling_japanese <- true;
		message requestFromInitiator <- (cfps at 0);
		do propose with: (message: requestFromInitiator, contents: ['I accept']);	
	 	write ' Auction selling was a success';		
		write ' shoe sold at: ' + (cd_price );
		mycolor<- #blue;
		}
		
	reflex failure_japanese_message when: !(empty(cfps)) and !motion and !japanese_auction_ended and !No_selling_japanese and (my_price_japanese <= cd_price) 
	   { message requestFromInitiator <- (cfps at 0);  	    
		 do refuse with: (message: requestFromInitiator, contents: []);  
		 }
	
	aspect default{
		draw sphere(4) at: location color: mycolor;
		draw geometry: 'Participant' + i color: #black  size: 2 at: {location.x-6,location.y-4} ;	

		}
	}
			
species selling_place {
	aspect default{
	  	draw pyramid(5) at: japanese_selling_position color: #black ;  	
	  	}
	}
	
experiment guests_assignment type: gui{
	output{
		display map type: opengl{
			species Participant ;
			species japanese_Initiator;
			species selling_place;
		}
	}	
}