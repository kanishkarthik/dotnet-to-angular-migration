namespace DotNetApp.Core.Configuration
{
    public interface IPropertyBuilder<TModel, TValue> where TModel : class
    {
        IPropertyBuilder<TModel, TValue> Type(string type);

        IPropertyBuilder<TModel, TValue> Name(string name);

        IPropertyBuilder<TModel, TValue> Required(bool required);

        IPropertyBuilder<TModel, TValue> Disabled(bool disabled);

        IPropertyBuilder<TModel, TValue> MaxLength(int maxLength);

        IPropertyBuilder<TModel, TValue> MinLength(int minLength);

        IPropertyBuilder<TModel, TValue> Pattern(string pattern);

    }
}
