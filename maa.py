from PIL import Image

def encode_image(image_path, secret_message, password):
    img = Image.open(image_path)
    encoded_img = img.copy()
    binary_secret = ''.join(format(ord(char), '08b') for char in secret_message)
    binary_secret += '1111111111111110'  # Adding a delimiter

    data_index = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = list(img.getpixel((i, j)))

            for color_channel in range(3):
                if data_index < len(binary_secret):
                    pixel[color_channel] = pixel [color_channel] & ~1 | int(binary_secret[data_index])
                    data_index += 1

            encoded_img.putpixel((i, j), tuple(pixel))
    encoded_img.save('encoded_image.png')
    print('Image encoded successfully.')

def decode_image(encoded_image_path, password):
    encoded_img = Image.open(encoded_image_path)

    binary_data = ''
    for i in range(encoded_img.size[0]):
        for j in range(encoded_img.size[1]):
            pixel = list(encoded_img.getpixel((i, j)))

            for color_channel in range(3):
                binary_data += str(pixel[color_channel] & 1)

    delimiter_index = binary_data.find('1111111111111110')
    secret_message_binary = binary_data[:delimiter_index]

    secret_number = input('Enter the secret number to decode the message: ')
    if secret_number == password:
        secret_message = ''.join(chr(int(secret_message_binary[i:i+8], 2)) for i in range(0, len(secret_message_binary),8))
        print('Decoded Message:', secret_message)
    else:
        print('Incorrect secret number. Decoding failed.')

# Example usage
image_path = input('Enter image path: ')
secret_message = input('Enter secret message: ')
password = input('Enter password (secret number): ')
encode_image(image_path, secret_message, password)
decode_image('encoded_image.png', password)