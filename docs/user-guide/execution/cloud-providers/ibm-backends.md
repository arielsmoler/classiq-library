# Execution on IBM Quantum Cloud

The Classiq executor supports execution on IBM simulators and hardware.

## Usage

### Execution on IBM Simulators

=== "SDK"

    [comment]: DO_NOT_TEST

    ```python
    from classiq import IBMBackendPreferences

    preferences = IBMBackendPreferences(backend_name="Name of requsted quantum simulator")
    ```

=== "IDE"

    ![Opening info tab](../../../resources/excution_ibm_simulation_login.png)

The supported simulators are fake hardware simulators.

### Execution on IBM Hardware

Execution on IBM hardware requires a valid IBM Quantum API access token, and access to the requested hardware with an IBM Quantum hub, group, and project name.
The access token is the API token that appears at the top of the [IBM Quantum Platform page](https://quantum-computing.ibm.com/), when you are logged in. You must create an account with IBM quantum if you do not have one already.

The hub, group and project default values refer to the open access quantum systems, and are:

-   hub = "ibm-q"
-   group = "open"
-   project = "main"

However, you may have your own hub, group, and project values through your organization. For more information, [see this FAQ](https://docs.quantum-computing.ibm.com/admin/faq-admin).

=== "SDK"

    [comment]: DO_NOT_TEST

    ```python
    from classiq import (
        IBMBackendPreferences,
        IBMBackendProvider,
    )

    ibm_provider = IBMBackendProvider(
        hub="Hub name", group="Group name", Project="Project name"
    )
    preferences = IBMBackendPreferences(
        backend_name="Name of requsted quantum hardware",
        access_token="A Valid API access token to IBM Quantum",
        provider=ibm_provider,
    )
    ```

=== "IDE"

    ![Opening info tab](../../../resources/excution_ibm_hardware_login.png)
