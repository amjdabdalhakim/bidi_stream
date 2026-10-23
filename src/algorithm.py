from unicodedata import bidirectional, mirrored
from .mirror import MIRRORED

def reshape_bidi_visual(text:str, base_direction:str='ltr', prefix:str='', strong_run_end:int=0, neutral_start:int=0, num_run_start:int=0, line_start:int=0):
    """
    Transforms logical text into visual order for bidirectional rendering (Optimized).
    """
    new_text:list = list(prefix) 
    
    # Local function caching for faster lookups in tight loops
    local_bidi = bidirectional
    local_mirrored = mirrored
    local_get = MIRRORED.get
    
    #RTL
    if base_direction == 'rtl':
        for char in text:
            bidi = local_bidi(char)
            if bidi in ('L', 'LRI'):#Strong LTR
                if num_run_start > strong_run_end:
                    strong_run_end = num_run_start
                if neutral_start > line_start: #Pick up the flaged neutrals
                    strong_run_end += (neutral_start - line_start)
                    new_text = new_text[:line_start] + new_text[neutral_start:strong_run_end] + new_text[line_start:neutral_start][::-1] + new_text[strong_run_end:]
                    neutral_start = line_start #Done
                new_text.insert(strong_run_end, char)
                strong_run_end += 1 #After
                
            elif bidi == 'NSM': #No size char
                if line_start == len(new_text):
                    new_text.insert(line_start, char)
                else:
                    new_text.insert(line_start + 1, char) #It comes after the char to be in the same place
                
            elif bidi in ('S', 'WS', 'ON', 'CS', 'ET', 'ES'): #Nuetrals
                if local_mirrored(char):
                    char = local_get(char, char) #Mirror
                    #This only mirror the neutrals in `base_direction == rtl` but it should be in any RTL case
                    
                new_text.insert(line_start, char) #Put as RTL for now
                if strong_run_end > line_start or num_run_start > line_start: #Active LTR (weak or strong)
                    
                    neutral_start += 1 #Flag a neutral after active LTR
                    
            elif bidi in ('EN', 'AN'): #Numbers
                if strong_run_end > num_run_start: #LTR already started from others then comlete with them
                    num_run_start = strong_run_end
                if neutral_start > line_start:
                    num_run_start += (neutral_start - line_start)
                    new_text = new_text[:line_start] + new_text[neutral_start:num_run_start] + new_text[line_start:neutral_start][::-1] + new_text[num_run_start:]
                    
                    #Before the line as it is, and the neutrals goes from RTL to LTR
                    
                    neutral_start = line_start
                new_text.insert(num_run_start, char)
                num_run_start += 1
            
            elif bidi == 'B': #Break/New Line
                new_text.append(char)
                #Every line has a start so the lines aren't reversed
                line_start = len(new_text)
                #Clear any Active
                strong_run_end = line_start
                neutral_start = line_start
                num_run_start = line_start
                           
            else: #Strong RTL/Others
                new_text.insert(line_start, char)
                #Clear
                strong_run_end = line_start
                neutral_start = line_start
                num_run_start = line_start
    #LTR
    else:
        for char in text:
            bidi = local_bidi(char)
            if bidi in ('R', 'AL', 'RLI'): #Strong RTL
                if neutral_start > 0:
                    new_text = new_text[:strong_run_end] + new_text[neutral_start:][::-1] + new_text[strong_run_end:neutral_start]
                    neutral_start = 0
                new_text.insert(strong_run_end, char)
            
            elif bidi == 'NSM':
                new_text.insert(strong_run_end + 1, char)
           
            elif bidi in ('S', 'WS', 'ON'):
                new_text.append(char)
                if strong_run_end != len(new_text) - 1: #Previous wasn't LTR
                    if neutral_start == 0:
                        neutral_start = len(new_text) - 1 #Flag the position
                else:
                    strong_run_end = len(new_text)
                   
            else:
                new_text.append(char)
                strong_run_end = len(new_text)
                neutral_start = 0
                
    return ''.join(new_text)