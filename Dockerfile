FROM devkitpro/devkitarm

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install apt-transport-https wget dirmngr build-essential git binutils-arm-none-eabi libsndfile1-dev libpng-dev python3 && curl -sL https://deb.nodesource.com/setup_10.x | bash - && apt-get -y install nodejs \
    && rm -rf /var/lib/apt/lists/*
COPY agbcc /agbcc
RUN cd /agbcc && ./build.sh && ./install.sh /agbcc_build
RUN mkdir -p /pretrepos && cd /pretrepos && git clone https://github.com/pret/pokeemerald && git clone https://github.com/pret/pokeruby && git clone https://github.com/pret/pokefirered
RUN cd /pretrepos/pokeemerald && make tools && cd /pretrepos/pokeruby && make tools && cd /pretrepos/pokefirered && make tools
RUN mkdir -p /frontends
COPY pycc.py /frontends/
COPY compiler-explorer /ce/
ENTRYPOINT cd /ce && make EXTRA_ARGS='--language C'