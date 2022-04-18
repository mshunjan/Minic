import asyncio 
from app.config.settings import settings

class Process():
    def __init__(self, inp, out_dir, input_type, filename):
        self.inp = inp
        self.out_dir = out_dir
        self.input_type = input_type
        self.bowtie_out =  "{}/{}{}".format(self.out_dir, filename,".bowtie2out.txt")
        self.mpa_out =  "{}/{}{}".format(self.out_dir, filename, ".out.txt")
        
        self.db = settings.MPA_DB
        self.cores =4
    
    def _command_generator(self):
        '''
        Generates commands for tool being run
        ''' 
        if self.input_type == 'bowtie2out':
             commands_lst = [
                "metaphlan",
                self.inp,
                "--input_type",
                self.input_type,
                "--nproc",
                self.cores,
                "-o",
                self.mpa_out
            ] 
        else:
            commands_lst = [
                "metaphlan",
                self.inp,
                "--input_type",
                self.input_type,
                "--bowtie2out",
                self.bowtie_out,
                "--nproc",
                self.cores,
                "-o",
                self.mpa_out,
                "--bowtie2db",
                self.db
            ] 

        return " ".join(str(x) for x in commands_lst)

    async def run(self):
        '''
        runs command in subprocess
        '''
        commands = self._command_generator()
        proc = await asyncio.create_subprocess_shell(
            commands,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()  
        if proc.returncode != 0:
            return stderr.decode()
        else:
            return stdout.decode() 