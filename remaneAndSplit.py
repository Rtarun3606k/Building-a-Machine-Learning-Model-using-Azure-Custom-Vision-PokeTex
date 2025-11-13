import os
import shutil
from sklearn.model_selection import train_test_split

def prepare_pokemon_dataset(root_path, output_path="pokemon_final", test_size=0.2):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    train_path = os.path.join(output_path, "train")
    test_path = os.path.join(output_path, "test")

    os.makedirs(train_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    # Loop through each Pokémon class folder
    for class_name in os.listdir(root_path):
        class_folder = os.path.join(root_path, class_name)

        if not os.path.isdir(class_folder):
            continue

        print(f"Processing {class_name}...")

        # Collect all image files
        images = [
            f for f in os.listdir(class_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        # Sort to keep consistent order
        images.sort()

        # Rename images
        renamed_images = []
        for idx, img in enumerate(images, 1):
            ext = os.path.splitext(img)[1]
            new_name = f"{class_name}_{idx:03d}{ext}"
            old_path = os.path.join(class_folder, img)
            new_path = os.path.join(class_folder, new_name)
            os.rename(old_path, new_path)
            renamed_images.append(new_name)

        # Train-test split
        train_imgs, test_imgs = train_test_split(
            renamed_images, test_size=test_size, random_state=42
        )

        # Create class dirs in output
        os.makedirs(os.path.join(train_path, class_name), exist_ok=True)
        os.makedirs(os.path.join(test_path, class_name), exist_ok=True)

        # Move images accordingly
        for img in train_imgs:
            shutil.copy(
                os.path.join(class_folder, img),
                os.path.join(train_path, class_name, img)
            )

        for img in test_imgs:
            shutil.copy(
                os.path.join(class_folder, img),
                os.path.join(test_path, class_name, img)
            )

    print("Dataset preparation complete!")


if __name__ == "__main__":
    root_dataset_path = "/home/dragoon/Downloads/PokemonData"  
    prepare_pokemon_dataset(root_dataset_path)
