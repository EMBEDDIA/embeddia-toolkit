import subprocess
import shlex
import os


class EMBEDDIABuilder:

    def __init__(self, dockerfiles):
        self.dockerfiles = dockerfiles
    

    def build(self):
        for dockerfile in self.dockerfiles:
            dockerfile_path = dockerfile[1]
            module_name = dockerfile[0]
            print(dockerfile_path)
            if os.path.exists(dockerfile_path):
                built = self.build_module(dockerfile_path, module_name)
            else:
                print("\nERROR: No Dockerfile present for module {}\n".format(module_name))


    @staticmethod
    def _call_process(process):
        while True:
            output = process.stdout.readline()
            if not output:
                break
            print(output.strip().decode())

    def build_module(self, dockerfile_path, module_name):
        build_context = os.path.dirname(dockerfile_path)
        build_command = "docker build -t {0} -f {1} {2}".format(module_name, dockerfile_path, build_context)
        print("Building {}...".format(module_name))
        process = subprocess.Popen(shlex.split(build_command), stdout=subprocess.PIPE)
        self._call_process(process)
        return True
    
    def push(self):
        # TODO: implement registry push
        pass


def main():
    try:
        dockerfiles = [
            ("embeddia-kwe", "modules/keyword/services/web/Dockerfile"),
            ("embeddia-nlg", "modules/nlg/Dockerfile"),
            ("embeddia-hsd", "modules/hatespeech/services/web/Dockerfile"),
            ("embeddia-rest", "src/Dockerfile")
        ]
        db = EMBEDDIABuilder(dockerfiles)
        built_id = db.build()
    except Exception as e:
        print("Build failed:", e)

if __name__ == "__main__": 
    main()
