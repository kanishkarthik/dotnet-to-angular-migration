namespace DotNetApp.Core.Configuration
{
    public class PropertyBuilder<TModel, TValue> : IPropertyBuilder<TModel, TValue>
        where TModel : class
    {
        private readonly Configuration configuration;

        public PropertyBuilder(Configuration configuration)
        {
            this.configuration = configuration;
        }

        public IPropertyBuilder<TModel, TValue> Disabled(bool disabled)
        {
            configuration.IsDisabled = disabled;

            return this;
        }

        public IPropertyBuilder<TModel, TValue> MaxLength(int maxLength)
        {
            configuration.MaxLength = maxLength;   

            return this;
        }

        public IPropertyBuilder<TModel, TValue> MinLength(int minLength)
        {
            configuration.MinLength = minLength;

            return this;
        }

        public IPropertyBuilder<TModel, TValue> Name(string name)
        {
            configuration.Name = name;

            return this;
        }

        public IPropertyBuilder<TModel, TValue> Pattern(string pattern)
        {
            configuration.Pattern = pattern;

            return this;
        }

        public IPropertyBuilder<TModel, TValue> Required(bool required)
        {
            configuration.IsRequired = required;

            return this;
        }

        public IPropertyBuilder<TModel, TValue> Type(string type)
        {
            configuration.Type = type;

            return this;
        }
    }
}
