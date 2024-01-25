class Transaction:

    @classmethod
    async def set_motor_cli(cls, motor_cli):
        cls.motor_cli = motor_cli

    @classmethod
    async def get_transaction(cls):
        return await cls.motor_cli.start_session()
