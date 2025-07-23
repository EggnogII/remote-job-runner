FROM rockylinux:9.3

# Run updates and dependencies
RUN yum update -y && yum upgrade -y

COPY requirements.txt .

RUN python3 -m venv venv && \
    venv/bin/pip3 install --no-cache-dir --upgrade pip && \
    venv/bin/pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x bootstrap.sh

EXPOSE 80

ENTRYPOINT ["bash", "./bootstrap.sh"]