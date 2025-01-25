import compare_img


option = input('Enter 1 to register a new user or 2 to verify an existing user: ')

if option == '1':
    user_id = input('Enter the user id: ')
    img_name = input('Enter the image name: ')
    img_path = "./images/" + img_name
    encoding = compare_img.load_and_encode_image(img_path)
    if encoding is None:
        print("can't detect a face.")
        exit()
    compare_img.save_user_image(img_name, user_id)
    print("User registered successfully.")
elif option == '2':
    img_name = input('Enter the image name: ')
    img_path = "./test_images/" + img_name
    encoding = compare_img.load_and_encode_image(img_path)
    if encoding is None:
        print("can't detect a face.")
        exit()
    user_id = compare_img.verify_user(encoding)
    if user_id:
        print(f"User {user_id} verified successfully.")
    else:
        print("User not found.")


