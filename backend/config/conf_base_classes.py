import dataclasses
import typing

T = typing.TypeVar("T")

class FieldInfo[T]:
    """Metadata about a dataclass field."""

    def __init__(self, 
                 name: str, 
                 value: T, 
                 is_explicit: bool, 
                 default_value: T):
        self.name = name
        self.value = value
        self._is_explicit = is_explicit
        self.default_value = default_value
    
    def is_default(self) -> bool:
        """Check if this field is using its default value."""
        return not self._is_explicit
    
    def is_explicit(self) -> bool:
        """Check if this field is using its default value."""
        return self._is_explicit

class FieldsProxy:
    """Container for field metadata that provides attribute-style access."""

    def __init__(self, instance: typing.Any, field_info: dict[str, FieldInfo]):
        self._instance = instance
        self._field_info = field_info
    
    def __getattr__(self, name: str) -> FieldInfo:
        if name in self._field_info:
            return self._field_info[name]
        raise AttributeError(f"No field named '{name}'")

class CustomDataclass:
    """Class wrapper for creating enhanced dataclasses with field tracking."""
    
    def __init__(self, cls: type[T]) -> None:
        if not isinstance(cls, type):
            raise TypeError(f"CustomDataclass expects a class, got {type(cls).__name__}")
        
        # Make it a dataclass if it isn't already
        if not dataclasses.is_dataclass(cls):
            cls = dataclasses.dataclass(cls, frozen=True)
        
        self.original_class = cls
        self.enhanced_class = self._enhance_class(cls)
    
    def _enhance_class(self, cls: type[T]) -> type[T]:
        """Create enhanced version of the class with field tracking."""
        assert dataclasses.is_dataclass(cls)
        # Get dataclass fields and their defaults
        fields = dataclasses.fields(cls)
        field_defaults = {}
        
        for field in fields:
            if field.default != dataclasses.MISSING:
                field_defaults[field.name] = field.default
            elif field.default_factory != dataclasses.MISSING:
                field_defaults[field.name] = field.default_factory()
            else:
                field_defaults[field.name] = None
        
        # Custom __init__ to handle explicit field tracking
        original_init = cls.__init__
        
        def __init__(self, *args, **kwargs):
            # Initialize field tracking
            field_info = {}
            field_names = [f.name for f in fields]
            
            # Mark all fields as default initially
            for field_name in field_names:
                field_info[field_name] = FieldInfo(
                    field_name,
                    field_defaults.get(field_name),
                    False,  # not explicit initially
                    field_defaults.get(field_name)
                )
            
            # Mark explicitly passed positional arguments
            for i, arg in enumerate(args):
                if i < len(field_names):
                    field_info[field_names[i]]._is_explicit = True
            
            # Mark explicitly passed keyword arguments
            for key in kwargs:
                if key in field_info:
                    field_info[key]._is_explicit = True
            
            # Store field info
            object.__setattr__(self, '_field_info', field_info)
            
            # Create the fields proxy
            object.__setattr__(self, '__fields__', FieldsProxy(self, field_info))
            
            # Call original init
            original_init(self, *args, **kwargs)
        
        def is_filled(self, field_name: str) -> bool:
            """Legacy method for dynamic field checking."""
            return self._field_info[field_name]._is_explicit
        
        # Create new class with modified __init__
        enhanced_cls = type(
            cls.__name__,
            cls.__bases__,
            {
                **cls.__dict__,
                '__init__': __init__,
                'is_filled': is_filled
            }
        )
        
        # Copy metadata
        enhanced_cls.__module__ = cls.__module__
        enhanced_cls.__qualname__ = cls.__qualname__
        
        return typing.cast(type, enhanced_cls)
    
    def __call__(self, *args, **kwargs) -> typing.Any:
        """Make the wrapper callable to create instances."""
        return self.enhanced_class(*args, **kwargs)
    
    def __getattr__(self, name: str) -> typing.Any:
        """Delegate attribute access to the enhanced class."""
        return getattr(self.enhanced_class, name)

# Decorator function
def custom_dataclass(cls: type[T]) -> type[T]:
    """Decorator function that returns the enhanced class."""
    wrapper = CustomDataclass(cls)
    return wrapper.enhanced_class # type: ignore