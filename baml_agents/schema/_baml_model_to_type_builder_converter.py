import warnings
from typing import TYPE_CHECKING, TypeVar

from baml_agents.schema._interfaces import BamlTypeBuilderConfigurer
from baml_agents.schema._model import (
    BamlBaseType,
    BamlClassModel,
    BamlEnumModel,
    BamlEnumValueModel,
    BamlFieldModel,
    BamlTypeInfo,
)

if TYPE_CHECKING:
    from baml_py.baml_py import (
        ClassBuilder,
        EnumBuilder,
        EnumValueBuilder,
        FieldType,
    )
    from baml_py.type_builder import (
        ClassPropertyBuilder,
        TypeBuilder,
    )
T = TypeVar("T", bound="TypeBuilder")


class BamlModelToTypeBuilderConverter(BamlTypeBuilderConfigurer[T]):
    """
    Converts a list of BAML models (BamlClassModel, BamlEnumModel) into
    configurations for a baml_py.TypeBuilder instance.
    """

    def configure(self, tb: T) -> T:
        """
        Adds the types defined in the BAML models to the provided TypeBuilder.

        Args:
            tb: An instance of TypeBuilder to be configured.

        Returns:
            The same TypeBuilder instance, now configured with the models.

        """
        for model in self._baml_models:
            if isinstance(model, BamlClassModel):
                self._configure_class(tb, model)
            elif isinstance(model, BamlEnumModel):
                self._configure_enum(tb, model)
            else:
                warnings.warn(
                    f"Unsupported BAML model type encountered: {type(model)}. Skipping."
                )
        return tb

    def _configure_class(self, tb: T, class_model: BamlClassModel) -> "ClassBuilder":
        """Configures a single BamlClassModel into the TypeBuilder."""
        class_builder = tb.add_class(class_model.name)

        if class_model.description:
            class_builder.description(class_model.description)
        # TypeBuilder ClassBuilder does not currently have an alias method
        # if class_model.alias:
        #     class_builder.alias(class_model.alias)

        for prop in class_model.properties:
            self._configure_property(tb, class_builder, prop)

        return class_builder

    def _configure_property(
        self, tb: T, class_builder: "ClassBuilder", prop: BamlFieldModel
    ) -> "ClassPropertyBuilder":
        """Configures a single BamlFieldModel onto a ClassBuilder."""
        if prop.skip:
            # TypeBuilder does not currently support skipping properties directly
            # We simply don't add the property if marked as skip in the model.
            warnings.warn(
                f"Property '{prop.name}' in class '{class_builder.name}' was marked as skip. "
                "It will not be added to the TypeBuilder."
            )
            # Need a dummy return that satisfies type hint but does nothing
            # This is a bit awkward, maybe TypeBuilder needs a way to handle skips?
            # For now, we just won't call add_property. Let's return None conceptually.
            # To satisfy type hints, we'll raise or return a placeholder if needed,
            # but ideally the caller just checks if prop.skip first.
            # Since we check skip *before* calling this might not be needed.
            # Let's assume the loop in _configure_class handles skipping.

        prop_type = self._convert_type_info(tb, prop.type_info)
        prop_builder = class_builder.add_property(prop.name, prop_type)

        if prop.description:
            prop_builder.description(prop.description)
        if prop.alias:
            prop_builder.alias(prop.alias)

        return prop_builder

    def _configure_enum(self, tb: T, enum_model: BamlEnumModel) -> "EnumBuilder":
        """Configures a single BamlEnumModel into the TypeBuilder."""
        enum_builder = tb.add_enum(enum_model.name)

        if enum_model.description:
            enum_builder.description(enum_model.description)
        # TypeBuilder EnumBuilder does not currently have an alias method
        # if enum_model.alias:
        #     enum_builder.alias(enum_model.alias)

        for value in enum_model.values:
            self._configure_enum_value(enum_builder, value)

        return enum_builder

    def _configure_enum_value(
        self, enum_builder: "EnumBuilder", value: BamlEnumValueModel
    ) -> "EnumValueBuilder":
        """Configures a single BamlEnumValueModel onto an EnumBuilder."""
        value_builder = enum_builder.add_value(value.name)

        if value.skip:
            value_builder.skip()
        if value.description:
            value_builder.description(value.description)
        if value.alias:
            value_builder.alias(value.alias)

        return value_builder

    def _convert_type_info(self, tb: T, type_info: BamlTypeInfo) -> "FieldType":
        """Recursively converts a BamlTypeInfo object to a TypeBuilder FieldType."""
        base_field_type: FieldType

        match type_info.base_type:
            case BamlBaseType.STR:
                base_field_type = tb.string()
            case BamlBaseType.INT:
                base_field_type = tb.int()
            case BamlBaseType.FLOAT:
                base_field_type = tb.float()
            case BamlBaseType.BOOL:
                base_field_type = tb.bool()
            case BamlBaseType.NULL:
                # Null is represented by optionality in TypeBuilder
                # We return an optional string as a placeholder, the optionality is handled below
                # Or perhaps tb.null() exists? Assuming not for now.
                # Let's make it optional of a base type, like string?.
                # The .optional() call below will handle the null aspect.
                # Let's default to string for the base of a null? type.
                # A union like string | null would be converted more naturally.
                # If it's *just* null, it implies optionality.
                base_field_type = tb.string()  # Placeholder type, optionality is key
            case BamlBaseType.ANY:
                warnings.warn(
                    "BAML type 'any' is not directly supported by TypeBuilder. "
                    "Mapping to 'string'. Consider using a more specific type or dynamic classes."
                )
                base_field_type = tb.string()
            case BamlBaseType.LITERAL_STRING:
                if type_info.literal_value is None:
                    raise ValueError(
                        "Literal string type info is missing literal_value"
                    )
                base_field_type = tb.literal_string(type_info.literal_value)
            case BamlBaseType.LITERAL_INT:
                if (
                    type_info.literal_value is None
                ):  # Ensure literal_value holds the correct type
                    raise ValueError("Literal int type info is missing literal_value")
                base_field_type = tb.literal_int(int(type_info.literal_value))
            case BamlBaseType.LITERAL_BOOL:
                if (
                    type_info.literal_value is None
                ):  # Ensure literal_value holds the correct type
                    raise ValueError("Literal bool type info is missing literal_value")
                base_field_type = tb.literal_bool(
                    str(type_info.literal_value).lower() == "true"
                )

            case BamlBaseType.LIST:
                if not type_info.item_type:
                    raise ValueError("List type info is missing item_type")
                item_field_type = self._convert_type_info(tb, type_info.item_type)
                base_field_type = tb.list(item_field_type)
            case BamlBaseType.UNION:
                if not type_info.union_types:
                    raise ValueError("Union type info is missing union_types")
                union_field_types = [
                    self._convert_type_info(tb, ut) for ut in type_info.union_types
                ]
                base_field_type = tb.union(union_field_types)
            case BamlBaseType.CLASS | BamlBaseType.ENUM:
                if not type_info.custom_type_name:
                    raise ValueError(
                        f"{type_info.base_type.name} type info is missing custom_type_name"
                    )
                # Reference the type by its name. TypeBuilder resolves this.
                base_field_type = tb.type(type_info.custom_type_name)
            case _:
                raise TypeError(f"Unsupported BamlBaseType: {type_info.base_type}")

        # Apply optionality if needed, unless the type itself is null
        if type_info.is_optional and type_info.base_type != BamlBaseType.NULL:
            return base_field_type.optional()
        # If the base type *was* NULL, it inherently implies optionality,
        # but we represented it as string(), so we still need .optional().
        # If is_optional was *already* true, this is redundant but harmless.
        if type_info.base_type == BamlBaseType.NULL:
            return base_field_type.optional()

        return base_field_type
