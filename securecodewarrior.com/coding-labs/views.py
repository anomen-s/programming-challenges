from rng_provider import RngProvider

token = RngProvider().generate_cryptographic_pseudo_random_string(128)

print(token)
