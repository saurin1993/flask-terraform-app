resource "aws_instance" "website" {
  ami           = "ami-0e86e20dae9224db8"
  instance_type = "t2.micro"

  vpc_security_group_ids = [ aws_security_group.my_instance_SG.id ]
  key_name      = "my-ec2-keypair"

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt install python3-pip -y
              sudo apt install python3-psutil -y
              sudo apt install python3-flask -y
              git clone https://github.com/saurin1993/flask-terraform-app.git
              cd flask-terraform-app
              python3 myapp.py &
              EOF

  tags = {
    Name = "my-python-app"
  }
}


//URL - http://my-python-app-ls-487385036.us-east-1.elb.amazonaws.com/