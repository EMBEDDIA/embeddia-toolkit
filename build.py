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
            if os.path.exists(dockerfile_path):
                built = self.build_module(dockerfile_path, module_name)
            else:
                print("\nERROR: No Dockerfile present for module {}\n".format(module_name))

    def build_module(self, dockerfile_path, module_name):
        build_context = os.path.dirname(dockerfile_path)
        build_command = "docker build -t {0} -f {1} {2}".format(module_name, dockerfile_path, build_context)
        print("Building {}...".format(module_name))
        process = subprocess.Popen(shlex.split(build_command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            
            if not output:
                break
            # print progress
            print(output.strip().decode())
        rc = process.poll()

        return True

        #built_id = built.communicate()[0].strip().split('\n')[-2].split()[-1]
        #print("Built {0}.".format(built_id))
        #return built_id


def main():
    try:
        dockerfiles = [
            ("embeddia-keyword", "modules/keyword/services/web/Dockerfile"),
            ("embeddia-nlg", "modules/nlg/Dockerfile"),
            ("embeddia-hatespeech", "modules/hatespeech/services/web/Dockerfile")
        ]
        db = EMBEDDIABuilder(dockerfiles)
        built_id = db.build()
    except Exception as e:
        print("Build failed:", e)

if __name__ == "__main__": 
    main()
