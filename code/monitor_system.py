import time                                                                                            
import serial                                                                                          
import datetime
                                                                                                       
class ReadCPXLine():                                                                                             
    def __init__(self, s):                                                                             
        self.buf = bytearray()                                                                         
        self.s = s                                                                                     
                                                                                                       
    def readline(self):                                                                                
        i = self.buf.find(b"\n")                                                                       
        if i >= 0:                                                                                     
            r = self.buf[:i+1]                                                                         
            self.buf = self.buf[i+1:]                                                                  
            return r                                                                                   
        while True:                                                                                    
            i = max(1, min(2048, self.s.in_waiting))                                                   
            data = self.s.read(i)                                                                      
            i = data.find(b"\n")                                                                       
            if i >= 0:                                                                                 
                r = self.buf + data[:i+1]                                                              
                self.buf[0:] = data[i+1:]                                                              
                return r                                                                               
            else:                                                                                      
                self.buf.extend(data)                                                                  
                                      
def get_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":

    ser = serial.Serial("/dev/ttyACM0", 115200, timeout=0.5)
    f = open("output.txt", "a")
    fe = open("errors.txt", "a")
    
    reader = ReadCPXLine(ser)
    x = reader.readline()
    while x:
        try:
            x = reader.readline()
            date_str = get_time()
            line = f"{date_str};{x.decode('utf-8')}"
            print(line)
            if "LOG" in line:
                f.write(line)
                f.flush()
            else:
                fe.write(line)
                fe.flush()
        except KeyboardInterrupt:
            print("Closing connection")
            f.close()
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            print(ser.is_open)
            time.sleep(1)
            ser.close()
            print(ser.is_open)
            break
