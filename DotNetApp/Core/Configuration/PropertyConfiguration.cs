using System;
using System.Linq.Expressions;

namespace DotNetApp.Core.Configuration
{
    public abstract class PropertyConfiguration<TModel> : Configuration where TModel : class
    {
        public TModel Model { get; set; }

        public PropertyConfiguration(TModel model)
        {
            Model = model;
        }

        public IPropertyBuilder<TModel, TReturn>
            ConfigureModel<TReturn>(Expression<Func<TModel, TReturn>> property)
        {
            var propertyConfig = new PropertyBuilderConfiguration<TModel, TReturn>(property);


            var added = AddConfiguration(property.ToString(), propertyConfig);
            added.Id = propertyConfig.PropertyName;

            return new PropertyBuilder<TModel, TReturn>(added);

        }

    }
}
