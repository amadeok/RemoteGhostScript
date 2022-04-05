import socket

from subprocess import Popen, PIPE, STDOUT
gs_bin = "C:\\Program Files\\gs\\gs9.55.0\\bin\\gswin64c.exe"

pcl_cmd = ["gpcl6win64.exe", "-sDEVICE=pdfwrite", "-sOutputFile=%stdout", "-q", "-"]
gs_ps_cmd = ["C:\\Program Files\\gs\\gs9.55.0\\bin\\gswin64c.exe", "-dCompatibilityLevel#1.4", "-q", "-P-", "-dSAFER", "-dNOPAUSE", "-dBATCH", "-sDEVICE#pdfwrite", '"-sOutputFile=%stdout"', "-dCompatibilityLevel#1.4", "-"]

print_cmd = [gs_bin, "-sDEVICE=mswinpr2", '"-sOutputFile=%printer%HP ENVY 4520 series [7C9A36]"', "-q", "-"]
#print_cmd = [gs_bin, "-sDEVICE=mswinpr2","-sPAPERSIZE=a4", '-dNOSAFER', "-dBATCH", "-dNOPAUSE", '-sOutputFile="%printer%"', "-"]

gs_cmd = ["C:\\Program Files\\gs\\gs9.55.0\\bin\\gswin64c.exe", "-dPrinted", "-dNoCancel", "-dNOPAUSE", "-dBATCH",  "-sPAPERSIZE=a4", "-sDEVICE=mswinpr2", #"-dBitsPerPixel=4" breaks it
"-sOutputFile=%printer%", "-q", "-"]
ps_print = [gs_bin, "-sDEVICE=mswinpr2", "-r600" "-dDownScaleFactor=3","-sPAPERSIZE=a4", '-dNOSAFER', "-dBATCH", "-dNOPAUSE", '"-sOutputFile=%printer%HP_MFP_135w"', "-"]
gs_ps_pdf = [gs_bin, "-dCompatibilityLevel#1.4",  "-P-", "-dNOSAFER", "-dNOPAUSE", "-dBATCH", "-sDEVICE#pdfwrite", "-sOutputFile=%stdout", '-sstdout=%stderr', "-q", "-"]

#gswin64c.exe -sDEVICE=mswinpr2 -dBATCH -dNOPAUSE -sOutputFile="%printer%\\printServer\printerNameWith Spaces" testprinter.ps

# HOST = '192.168.1.230'  # Standard loopback interface address (localhost)
# PORT = 9595        # Port to listen on (non-privileged ports are > 1023)
REM_HOST = '95.234.158.110'  # Standard loopback interface address (localhost)
REM_PORT = 27427     # Port to listen on (non-privileged ports are > 1023)
print ("started")
import time
print_ps_directly = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to " + REM_HOST + ":" + str(REM_PORT))
    s.connect((REM_HOST, REM_PORT))
    print("Socket connected")
    while 1:
          size_b = s.recv(4)
          size = int.from_bytes(size_b, 'little')
          print("receving " + str(size) + " bytes")
          #while True:
          #data = conn.recv(size)


          recv_data=[]
          recv_data = b''
          rem = size
          buf = 500
          while True:
            data=s.recv(buf)
            rem-= len(data)
            if (rem < 500):
              buf = rem

            

            l =  0
           # for ch in recv_data:
              #l += len(ch)
            recv_data +=data;
            l = len(recv_data)
            if not data or l >= size:
              break

            #recv_data.append(data)
          #recv_data=''.join(recv_data)

          recv_size = len(recv_data)
          if recv_size != size:
            print("error dif size")
          # if not data:
          #     break
          s.sendall(recv_data) 
         # conn.send(data)
          #time.sleep(1)
          re = s.recv(1)
          print(re)
          f=open('I_recved_this.Ps','wb')

          f.write(recv_data)
          f.flush()
          f.close()
          
          if print_ps_directly:
            print("running :"  + str(ps_print))
            p = Popen(ps_print, stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
            grep_stdout = p.communicate(input=recv_data)[0]

          else:
            p = Popen(gs_ps_pdf, stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
            grep_stdout = p.communicate(input=recv_data)[0]

            f=open('converted.pdf','wb')
            f.write(grep_stdout)
            f.flush()

            p.wait()
            print("to pdf")
            grep_stdout = grep_stdout[37:-1]

                # # with open("convertedfixed.pdf", "rb") as inp:
                # #     data = inp.read()

                # f=open('convertedf.pdf','wb')
                # f.write(grep_stdout)
                # f.flush()

            p = Popen(print_cmd,  stdout=PIPE, stdin=PIPE, stderr=STDOUT)      
            grep_stdout2 = p.communicate(input=grep_stdout)[0]
            print(grep_stdout2)
            p.wait()




        #   f=open('I_recved_this.pdf','wb')

        #   f.write(grep_stdout)
        #   f.flush()

        #   p.wait()
        #   print("\n running :"  + str(gs_cmd))
        #   p = Popen(gs_cmd, stdin=PIPE)    
        #   grep_stdout2 = p.communicate(input=grep_stdout)[0]



				  #f.flush()

          #COPY /B "I_printed_this .pcl" \\DESKTOP-667P6LG\Xerox