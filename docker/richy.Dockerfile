FROM python:3.11-slim

ARG USERNAME=richy
ARG MY_APP=richy
WORKDIR /app/${MY_APP}

# Create user
USER root
RUN apt-get update &&\
    apt-get install --yes --no-install-suggests --no-install-recommends \
        # basics
        ca-certificates \
        git \
        less \
        openssh-client \
        vim \
        \
    &&\
    apt-get clean
RUN useradd --system --create-home --shell /bin/bash ${USERNAME}
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    # && apt-get update \
    # && apt-get install -y sudo \
    # && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    # && chmod 0440 /etc/sudoers.d/$USERNAME

# Let's get it started yeah
USER ${USERNAME}
WORKDIR /workdir


# Install dependencies
RUN pip install --no-cache-dir 'richy @ git+https://github.com/dominicparga/richy.git@stable'
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# Expose the port the app runs on
EXPOSE 80

# credits 8)
LABEL maintainer="dominic.parga@icloud.com"
LABEL description="Financing"

ENTRYPOINT [ "richy" ]
CMD [ "-h"]
