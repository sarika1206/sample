""" Develop a Commandline utility for building simple AWS environment....."""
#!/usr/bin/env python
import os
import string
import random
import boto3
import click
import json


class AwsTool:
    """This is the class to develop a Commandline utility for building simple AWS environment"""

    def template(output, compute_type):
        """
        In this method we are creating the template and coping it to output foler
        :param output: output is the folder path where we are coping the template and default is "."
        :param compute_type: compute type is the type of instnce we are creating default is "t2.micro"
        """
        #we are reading PYTHONPATH from environment variable
        python_path = os.environ['PYTHONPATH']
        folder = "."
        filename = "cloudformation.json"
        template_file = os.path.join(python_path, "templates", filename)
        # if user is giving output folder to copy the template in commandline 
        if output:
            folder = output
        with open(template_file) as f:
            data = json.load(f)
        # if user is giving instnce type to be used it will change the default instnce type
        if compute_type:
            data['Parameters']['InstanceType']['Default'] = compute_type
        # creating a template file in output folder and writing the content 
        f = open(os.path.join(folder, filename), 'w')
        f.write(json.dumps(data))
        f.close()
        print("Successfully copied template to output folder")

    @click.command()
    @click.option('--compute-type', '-c', help="compute machine type (default: t2.micro)")
    @click.option('--region', '-r', help="environment region (default: us-west-1)")
    @click.option('--output', '-o', help="directory to store template (used with -t option) (default: .)")
    @click.option('--generate-template', '-t', is_flag=True,
                  help="cloud formation template with customized region,compute-type and/or name")
    @click.option('--help', '-h', is_flag=True, help="Will print help messages.")
    @click.option('--deploy', '-d', is_flag=True, help="create cloud formation template")
    @click.option('--name', '-n', help="stack name (default : cf-(autogen))")
    def aws_tool(name, deploy, help, generate_template, output, region, compute_type):
        """
        In this method we are deploying the template.
        :return:
        """
        python_path = os.environ['PYTHONPATH']
        folder = "."
        filename = "cloudformation.json"
        template_file = os.path.join(python_path, "templates", filename)
        # it will print the help content with the -h or --help
        if help:
            click.echo("-h / --help prints available options \n"
                       "-n / --name stack name (default : cf-(autogen)) \n"
                       "-c / --compute_type compute machine type (default: t2.micro) \n"
                       "-r / --region environment region (default: us-west-1) \n"
                       "-t / --generate-template-only output only cloud formation template "
                       "with customized region, compute-type and/or name \n"
                       "-d / --deploy create cloud formation template \n"
                       "-o / --output {folder } directory to store template (used with -t option) (default: .)")
            exit()
        stack = 'cf-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        # if user is giving the stack name to be used else it will use default stack name
        if name:
            stack = name
        if generate_template:
            AwsTool.template(output, compute_type)
            exit()

        client = boto3.client('cloudformation')
        # we are deploying the template to cloudformation
        if deploy:
            if not generate_template:
                AwsTool.template(output, compute_type)
            with open(os.path.join(folder, filename), 'r') as f:
                data = f.read()
            try:
                client.create_stack(StackName=stack, TemplateBody=data,
                                    Parameters=[{"ParameterKey": "ec2keypair", "ParameterValue": "kubernetes"}],
                                    Capabilities=['CAPABILITY_IAM'])
                print("Successfully deploy the cloudformation template")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    aws = AwsTool()
    aws.aws_tool()

