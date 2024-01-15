# LockBox PrivateLink

LockBox PrivateLink is a locally hosted webapp that is used to encrypt and decrypt files and text messages, aswell as sending the encryption key securely.

> **Note:** This is only tested on Windows 11

## Table of Contents
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
- [Usage](#usage)
  - [Starting the Application](#starting-the-application)
  - [Securely Sharing the `secret-key`](#securely-sharing-the-secret-key)
  - [Encrypt and decrypt messages and files](#encrypt-and-decrypt-messages-and-files)
- [API Reference](#api-reference)
- [Contributing](#contributing)
  - [Bug Reports](#bug-reports)
  - [Feature Requests](#feature-requests)
  - [Code Contributions](#code-contributions)
- [Credits](#credits)
  - [Contributors](#contributors)
  - [Third-Party Libraries](#third-party-libraries)
- [License](#license)


## Installation

### Prerequisites
#### Precompiled (exe) Version:
- Windows

#### Source/Development Version:
- Python 3.10.9 or later
- git

### Installation Steps

#### Precompiled (exe) Version:
1. Download zip from releases
2. Extract at a desired location
3. Run LockBox-PrivateLink.exe

#### Source/Development Version:

1. Clone the Repository:

    ```bash
    git clone https://github.com/McEsgow/LockBox-PrivateLink
    cd LockBox-PrivateLink
    ```

2. Set Up Virtual Environment and Install Dependencies:

    For Windows: Run `create-venv.bat` or the following commands:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    python -m pip install -r requirements.txt
    ```

    For macOS/Linux:
    ```bash
    python -m venv venv
    source venv/bin/activate
    python -m pip install -r requirements.txt
    ```

## Usage

### Starting the Application

#### Precompiled (exe) Version (Windows):
1. Run `webui.exe`.
2. Open [http://127.0.0.1:58538](http://127.0.0.1:58538) in a web browser.

#### Source/Development Version (Windows):
1. Run `webui.bat` or the following commands:
   ```bash
   cd [INSTALLATION PATH]/LockBox-PrivateLink/
   .\venv\Scripts\activate
   python webui.py
   ```
2. Open [http://127.0.0.1:58538](http://127.0.0.1:58538) in a web browser.

#### Source/Development Version (macOS/Linux):
1. Run the following commands:
   ```bash
   cd [INSTALLATION PATH]/LockBox-PrivateLink/
   source venv/bin/activate
   python webui.py
   ```
2. Open [http://127.0.0.1:58538](http://127.0.0.1:58538) in a web browser.


### Securely Sharing the `secret-key`
To encrypt and decrypt files and messages using LockBox, both parties need the same `secret-key`. To ensure the `secret-key` remains confidential, use PrivateLink to securely exchange it.

1. Agree upon who will be the **Key Receiver** and who will be the **Key Sender**.

#### PrivateLink Section:

2. **Key Receiver**: Generate a private and `public key` pair and share the `public key` with the **Key Sender**. 
    > **Note:** Do not share the private key with anyone!

3. **Key Sender**: Generate a `secret-key`, encrypt it using the **Key Receiver**'s `public key`, and share the encrypted `secret-key` with the **Key Receiver**.

4. **Key Receiver**: Decrypt the encrypted `secret-key` using their private key.

Now, both parties have the same `secret-key`.

> **Note:** The `secret-key` is not saved. Both parties will have to do that manually.


### Encrypt and Decrypt Messages and Files

Now that both parties share the same `secret-key`, you can securely encrypt and decrypt messages and files using LockBox.

#### Encrypt Files

1. **Select a File**:
   - Drag and drop a file into the designated area or manually choose a file.

2. **Encrypt File**:
   - Click the "Encrypt File" button to encrypt the selected file.
      - The encrypted file is saved as `[File name].[File extension].lb`.
      - The encrypted file is automatically copied to the clipboard.

#### Decrypt Files

1. **Select an Encrypted File**:
   - Drag and drop an encrypted file into the designated area or manually choose a file.
      - Only files with the `.lb` file extension can be decrypted.

2. **Decrypt File**:
   - Click the "Decrypt File" button to decrypt the selected file.
      - The decrypted file is saved with the original filename, excluding the `.lb` extension.
      - Incorrect decryption keys will result in corrupted file data.

> **Note:** Access the storage location for encrypted and decrypted files from a button in the web UI under the encrypt and decrypt file buttons.
> 
> Alternatively:
> - Source/Development Version: `[INSTALLATION PATH]/LockBox-PrivateLink/LockBox/`
> - Precompiled (exe) Version: `[INSTALLATION PATH]/LockBox-PrivateLink/_internal/LockBox/`

#### Encrypt and Decrypt Text Messages

1. **Enter Text**:
   - Input plaintext or encrypted text into the text area.

2. **Text Operations**:
   - Click "Encrypt Text" or "Decrypt Text" to perform the corresponding operation.
      - The text area will be replaced with the result (encrypted or decrypted text).


## Contributing

I welcome contributions from the community to improve and enhance this project. Here's how you can contribute:

### Bug Reports

If you encounter any issues or bugs while using the project, please [create a new issue](https://github.com/McEsgow/LockBox-PrivateLink/issues) with a detailed description. Include information such as steps to reproduce, expected behavior, and your environment.

### Feature Requests

If you have ideas for new features or improvements, feel free to [submit a feature request](https://github.com/McEsgow/LockBox-PrivateLink/issues). Provide a clear description of the proposed feature and any relevant context or use cases.

### Code Contributions

I appreciate code contributions to fix bugs or add new features. If you'd like to contribute code, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and ensure the code is well-documented.
4. Test your changes thoroughly.
5. Submit a pull request, explaining the purpose of your changes and any considerations for reviewers.

I may review your contributions and work with you to ensure they align with the project's goals. Thank you for considering contributing to my project!


## Credits

### Contributors
- Eskil Westdahl

### Third-Party Libraries
- [jQuery](https://jquery.com/)
  - Link: `<script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>`

- [Cryptography](https://cryptography.io/)
  - Used for cryptographic operations.
  - Python code imports:
    ```python
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    ```

- [Flask](https://flask.palletsprojects.com/)
  - Used for building web applications with Python.
  - Python code imports:
    ```python
    from flask import Flask, render_template, request, jsonify, send_from_directory
    ```

## License

### [LockBox PrivateLink](https://github.com/McEsgow/LockBox-PrivateLink) © 2024 by [Eskil Westdahl](https://github.com/McEsgow) is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).


#### You are free to:

-  **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material
- The licensor cannot revoke these freedoms as long as you follow the license terms.

#### Under the following terms:

- **Attribution** — You must give [appropriate credit][1], provide a link to the license, and [indicate if changes were made][2]. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

- **NonCommercial** — You may not use the material for [commercial purposes][3] .

- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the [same license][4] as the original.

    **No additional restrictions** — You may not apply legal terms or [technological measures][5] that legally restrict others from doing anything the license permits.

#### Notices:

You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable [exception or limitation][6].

No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as [publicity, privacy, or moral rights][7] may limit how you use the material.

### Footnotes
[1]: **appropriate credit** — If supplied, you must provide the name of the creator and attribution parties, a copyright notice, a license notice, a disclaimer notice, and a link to the material. CC licenses prior to Version 4.0 also require you to provide the title of the material if supplied, and may have other slight differences. [More Info](https://wiki.creativecommons.org/wiki/License_Versions#Detailed_attribution_comparison_chart) 

[2]: **indicate if changes were made** — In 4.0, you must indicate if you modified the material and retain an indication of previous modifications. In 3.0 and earlier license versions, the indication of changes is only required if you create a derivative. [Marking guide](https://wiki.creativecommons.org/wiki/Best_practices_for_attribution#This_is_a_good_attribution_for_material_you_modified_slightly), [More info](https://wiki.creativecommons.org/wiki/License_Versions#Modifications_and_adaptations_must_be_marked_as_such).

[3]: **commercial purposes** — A commercial use is one primarily intended for commercial advantage or monetary compensation. [More info](https://creativecommons.org/faq/#does-my-use-violate-the-noncommercial-clause-of-the-licenses).

[4]: **same license** — You may also use a license listed as compatible at https://creativecommons.org/compatiblelicenses. [More info](https://creativecommons.org/faq/#if-i-derive-or-adapt-material-offered-under-a-creative-commons-license-which-cc-licenses-can-i-use).

[5]: **technological measures** — The license prohibits application of effective technological measures, defined with reference to Article 11 of the WIPO Copyright Treaty. [More info](https://wiki.creativecommons.org/wiki/License_Versions#Application_of_effective_technological_measures_by_users_of_CC-licensed_works_prohibited).

[6]: **exception or limitation** — The rights of users under exceptions and limitations, such as fair use and fair dealing, are not affected by the CC licenses. [More info](https://creativecommons.org/faq/#Do_Creative_Commons_licenses_affect_exceptions_and_limitations_to_copyright.2C_such_as_fair_dealing_and_fair_use.3F).

[7]: **publicity, privacy, or moral rights** — You may need to get additional permissions before using the material as you intend. [More info](https://wiki.creativecommons.org/wiki/Considerations_for_licensors_and_licensees).
