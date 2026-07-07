# Based on standard UV Docker setup https://docs.astral.sh/uv/guides/integration/docker

FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

COPY . /app

# Disable development dependencies
ENV UV_NO_DEV=1


# USER nobody
# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app


# # Enable bytecode compilation
# ENV UV_COMPILE_BYTECODE=1

# # Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# # Ensure installed tools can be executed out of the box
# ENV UV_TOOL_BIN_DIR=/usr/local/bin



# # Download dependencies as a separate step to take advantage of Docker's caching.
# # Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# # Leverage a bind mount to requirements.txt to avoid having to copy them into
# # into this layer.
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --locked --no-install-project --no-dev
RUN uv sync --locked


# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

RUN chown -R nonroot:nonroot /app \
 && chmod -R +r /app

ENV PATH="/app/.venv/bin:$PATH"

RUN python manage.py collectstatic --noinput

RUN chmod +x /app/entrypoint.sh

# RUN chown -R nobody:nogroup /usr/src/app \
#  && chmod -R +r /usr/src/app

USER nonroot

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uv", "run", "streamlit", "run", "direct_framework_data_analysis_streamlit_app/analyse_multi_user_data.py", "--server.port", "8000", "--server.address", "0.0.0.0"]
