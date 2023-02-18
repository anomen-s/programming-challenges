from django.contrib.auth.hashers import Argon2PasswordHasher


class CustomArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = 2 * Argon2PasswordHasher.time_cost
    memory_cost = 2 * Argon2PasswordHasher.memory_cost
    parallelism = 2 * Argon2PasswordHasher.parallelism
    salt_entropy = 2 * Argon2PasswordHasher.salt_entropy
