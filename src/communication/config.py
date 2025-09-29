# python
class KafkaConfig:
    ENV_CONFIGS = {
        'local': {
            'bootstrap.servers': 'localhost:8000',
            'group.id': 'local-test-group'
        },
        'staging': {
            'bootstrap.servers': 'icicle-uca-dev-1.tacc.cloud:9094',
            'group.id': 'local-test-group',
            'security.protocol': 'SSL',
            'ssl.endpoint.identification.algorithm': 'none',
            'enable.ssl.certificate.verification': False
        },
        'prod': {
            'bootstrap.servers': ''
        }
    }

    @classmethod
    def get_conf(cls, env: str) -> dict:
        base = cls.ENV_CONFIGS.get(env)
        if base is None:
            raise ValueError(f"Unknown Kafka environment: {env}")
        return {
            **base,
            'client.id': __import__('socket').gethostname()
        }