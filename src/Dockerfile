FROM continuumio/miniconda3:latest

# Copy environment file
COPY environment.yaml /var/environment.yaml

RUN set -x \
    && conda env create -f /var/environment.yaml \
    && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

# Copy project files
COPY . /var/embeddia-rest

# Ownership to www-data and entrypoint
RUN chown -R www-data:www-data /var/embeddia-rest \
    && chmod 775 -R /var/embeddia-rest \
    && chmod 777 -R /opt/conda/envs/embeddia-rest \
    && chmod +x /var/embeddia-rest/entrypoint.sh \
    && rm -rf /var/embeddia-rest/.git \
    && rm -rf /root/.cache

# System configuration files
COPY supervisord.conf /opt/conda/envs/embeddia-rest/etc/supervisord/conf.d/supervisord.conf
ENV UWSGI_INI /var/embeddia-rest/embeddia-rest.ini

# Set environment variables
ENV PYTHONIOENCODING=UTF-8
ENV UWSGI_CHEAPER 2
ENV UWSGI_PROCESSES 16

# Expose ports
EXPOSE 80
EXPOSE 8000
EXPOSE 8001

# Ignition!
WORKDIR /var/embeddia-rest
ENTRYPOINT ["/var/embeddia-rest/entrypoint.sh"]
CMD ["supervisord", "-n"]
