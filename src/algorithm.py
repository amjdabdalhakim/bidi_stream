from unicodedata import bidirectional, mirrored
from .mirror import MIRRORED

def reshape_bidi_visual(text, base_direction='ltr', prefix='', strong_run_end=0, neutral_start=None, num_run_start=0, line_start=0):
    """
    Transforms logical text into visual order for bidirectional rendering (Optimized).
    """
    new_text = list(prefix) 
    
    # Local function caching for faster lookups in tight loops
    local_bidi = bidirectional
    local_mirrored = mirrored
    local_get = MIRRORED.get
    
    if base_direction == 'rtl':
        for char in text:
            bidi = local_bidi(char)
            if bidi in ('L', 'LRI'):  
                if neutral_start is not None:
                    new_text = new_text[:line_start] + new_text[neutral_start:strong_run_end] + new_text[line_start:neutral_start][::-1] + new_text[strong_run_end:]
                    neutral_start = None
                new_text.insert(strong_run_end, char)
                strong_run_end += 1
                
            elif bidi == 'NSM':
                new_text.insert(line_start + 1, char)
                
            elif bidi in ('S', 'WS', 'ON'):
                if local_mirrored(char):
                    char = local_get(char, char)
                new_text.insert(line_start, char)
                if not strong_run_end == line_start:
                    if neutral_start is None:
                        neutral_start = line_start
                    neutral_start += 1
                    strong_run_end += 1
                    
            elif bidi in ('EN', 'AN', 'ES', 'CS'): 
                if neutral_start is not None:
                    new_text = new_text[:line_start] + new_text[neutral_start:num_run_start] + new_text[line_start:neutral_start][::-1] + new_text[num_run_start:]
                    neutral_start = None 
                new_text.insert(num_run_start, char)
                num_run_start += 1
            
            elif bidi == 'B':
                new_text.append(char)
                line_start = len(new_text)
                strong_run_end = line_start
                neutral_start = None
                num_run_start = line_start
                           
            else:
                new_text.insert(line_start, char)
                strong_run_end = line_start
                neutral_start = None
                num_run_start = line_start
    else:
        for char in text:
            bidi = local_bidi(char)
            if bidi in ('R', 'AL', 'RLI'):
                if neutral_start is not None:
                    new_text = new_text[:strong_run_end] + new_text[neutral_start:][::-1] + new_text[strong_run_end:neutral_start]
                    neutral_start = None
                new_text.insert(strong_run_end, char)
            
            elif bidi == 'NSM':
                new_text.insert(strong_run_end + 1, char)
           
            elif bidi in ('S', 'WS', 'ON'):
                new_text.append(char)
                if not strong_run_end == len(new_text) - 1:
                    if neutral_start is None:
                        neutral_start = len(new_text) - 1
                else:
                    strong_run_end = len(new_text)
                   
            else:
                new_text.append(char)
                strong_run_end = len(new_text)
                neutral_start = None
                
    return ''.join(new_text)
