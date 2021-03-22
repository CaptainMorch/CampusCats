{
    const DefaultListField = {
        init: function() {
            Array.from(document.getElementsByClassName("default-lf")
                ).forEach(element => {
                    DefaultListField.initElements(element.firstElementChild);
                });
        },
        deleteElement: function(buttonElement) {
            const element = buttonElement.parentElement;
            const root = element.parentElement;
            element.parentElement.removeChild(element);
            DefaultListField.updateValue(root);
        },
        displayElement: function(root, content) {
            const newElement = root.getElementsByClassName(
                "default-lf-template")[0].cloneNode(true);
            newElement.className = "default-lf-element";
            newElement.firstElementChild.textContent = content;

            root.appendChild(newElement);
        },
        addElement: function(buttonElement) {
            const inputElement = buttonElement.previousElementSibling;
            const root = buttonElement.parentElement.parentElement;
            DefaultListField.displayElement(root, inputElement.value);
            inputElement.value = "";
            DefaultListField.updateValue(root);
        },
        initElements: function(inputElement) {
            const root = inputElement.parentElement;
            const sep = inputElement.getAttribute("data-sep");
            const value = inputElement.value;
            if (value && value!= sep+sep) {
                const elements = value.split(sep).slice(1, -1);
                elements.forEach(element => {
                    DefaultListField.displayElement(root, element);
                });
            }
        },
        updateValue: function(root) {
            const hiddenInput = root.firstElementChild;
            const sep = hiddenInput.getAttribute("data-sep");
            const elements = Array.from(
                    root.getElementsByClassName("default-lf-element")
                ).map(
                    element => element.firstElementChild.textContent
                );
            hiddenInput.value = sep + elements.join(sep) + sep;

            console.log(hiddenInput.value);
        }
    };

    window.addEventListener("load", DefaultListField.init);
    window.DefaultListField = DefaultListField;
}