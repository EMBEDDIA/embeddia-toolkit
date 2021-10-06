FROM continuumio/miniconda3:latest

# Copy environment file
COPY environment.yaml /var/environment.yaml

RUN set -x \
    && conda env create -f /var/environment.yaml \
    && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

# create project dir
RUN mkdir /var/embeddia-rest
# copy entrypoint
COPY ./entrypoint.sh /var/embeddia-rest/entrypoint.sh
# copy source
COPY . /var/embeddia-rest/src

# Retrieve pre-built front
RUN wget https://packages.texta.ee/embeddia-front/embeddia-front-latest.tar.gz --no-check-certificate \
    && tar -zxvf embeddia-front-latest.tar.gz \
    && cp -r dist/embeddia-front /var/embeddia-rest/front \
    && rm embeddia-front-latest.tar.gz && rm -R dist

# create data dir for MLP
RUN mkdir /var/embeddia-rest/data

# Ownership to www-data and entrypoint
RUN chown -R www-data:www-data /var/embeddia-rest \
    #&& chmod 775 -R /var/embeddia-rest \
    #&& chmod 777 -R /opt/conda/envs/embeddia-rest \
    && chmod +x /var/embeddia-rest/entrypoint.sh \
    && rm -rf /var/embeddia-rest/src/.git \
    && rm -rf /root/.cache

# System configuration files
COPY ./supervisord.conf /opt/conda/envs/embeddia-rest/etc/supervisord/conf.d/supervisord.conf
COPY ./nginx.conf /opt/conda/envs/embeddia-rest/etc/nginx/sites.d/default-site.conf
ENV UWSGI_INI /var/embeddia-rest/src/embeddia-rest.ini

# Set environment variables
ENV PYTHONIOENCODING=UTF-8
ENV UWSGI_CHEAPER 2
ENV UWSGI_PROCESSES 16

# Expose ports
EXPOSE 80
EXPOSE 8000
EXPOSE 8001

# Ignition!
WORKDIR /var/embeddia-rest/src
ENTRYPOINT ["/var/embeddia-rest/entrypoint.sh"]
CMD ["supervisord", "-n"]
