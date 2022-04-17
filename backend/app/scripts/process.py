import asyncio 
import pandas as pd
from app.config.settings import settings

class Process():
    def __init__(self, inp, out_dir, input_type):
        self.inp = inp
        self.out_dir = out_dir
        self.input_type = input_type
        self.bowtie_out =  "{}/{}".format(self.out_dir, "bowtie2.out")
        self.mpa_out =  "{}/{}".format(self.out_dir, "out.txt")
        
        self.db = settings.MPA_DB
    
    def _command_generator(self):
        '''
        Generates commands for tool being run
        ''' 
        commands_lst = [
                "metaphlan",
                self.inp,
                "--input_type",
                self.input_type,
                "--bowtie2out",
                self.bowtie_out,
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