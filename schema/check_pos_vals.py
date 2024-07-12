
all_added = [
(1,     'None'),	         
(2,     'disarmed'),	     
(3,     'armed_home'),	     
(4,     'armed_away'),	     
(5,     'armed_night'),	     
(6,     'armed_vacation'),	 
(7,     'armed_custom_bypass'),
(8,     'pending'),	         
(9,     'arming'),	         
(10,    'disarming'),	     
(11,    'triggered'),        
(12,    'unknown'),	         
(13,    'unavailable'),      
(14,    'on'),	             
(15,    'off'),	             
(16,    'pressed'),          
(17,    'idle'),             
(18,    'recording'),        
(19,    'streaming'),        
(20,    'auto'),             
(21,    'cool'),             
(22,    'heat'),             
(23,    'heat_cool'),        
(24,    'dry'),              
(25,    'fan_only'),         
(26,    'preheating'),       
(27,    'heating'),          
(28,    'cooling'),          
(29,    'drying'),           
(30,    'fan'),              
(31,    'defrosting'),       
(32,    'fan_on'),           
(33,    'fan_off'),          
(34,    'fan_auto'),         
(35,    'fan_low'),          
(36,    'fan_medium'),       
(37,    'fan_high'),         
(38,    'fan_middle'),       
(39,    'fan_focus'),        
(40,    'fan_diffuse'),      
(41,    'swing_off'),        
(42,    'swing_on'),         
(43,    'swing_vertical'),   
(44,    'swing_horizontal'), 
(45,    'swing_both'),       
(46,    'text'),             
(47,    'closed'),           
(48,    'closing'),          
(49,    'open'),             
(50,    'opening')                  
]

possible_values = dict()
    
for e in all_added:
    if e[1] not in possible_values:
        possible_values[e[1]] = e[0]

print(len(possible_values.items()))

counter = 1

for e in possible_values:
    if counter > 1:
        while possible_values[e] > counter:
            print(counter)
            counter += 1 
    counter += 1
