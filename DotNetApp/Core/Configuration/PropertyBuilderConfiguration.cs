using System;
using System.Linq.Expressions;
using System.Web.Mvc;

namespace DotNetApp.Core.Configuration
{
    public class PropertyBuilderConfiguration<TModel, TProperty> : Configuration where TModel : class
    {
        public string PropertyName { get; set; }
        public Func<string> DisplayName { get; set; }
        public Func<string> ControlType { get; set; }
        public Func<bool> IsRequired { get; set; }
        public Func<bool> IsDisabled { get; set; }
        public Func<string> Pattern { get; set; }
        public Func<int, int> MinLength { get; set; }
        public Func<int, int> MaxLength { get; set; }


        public override void ConfigureModel()
        {
            throw new System.NotImplementedException();
        }

        public PropertyBuilderConfiguration(Expression<Func<TModel, TProperty>> expression)
        {
           PropertyName = ExpressionHelper.GetExpressionText(expression);
            DisplayName = () => PropertyName;
            ControlType = () => "text";
            IsRequired = () => false;
            IsDisabled = () => false;
            Pattern = () => "";
            MinLength = (length) => length;
            MaxLength = (length) => length;
        }
    }
}