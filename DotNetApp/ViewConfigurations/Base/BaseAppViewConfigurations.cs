using Application.ViewModels.ASIA.India.BKT;
using DotNetApp.Core.Configuration;
using DotNetApp.ViewModels.Base;
using System;

namespace DotNetApp.ViewConfigurations.Base
{
    public class BaseAppViewConfigurations<TModel> : PropertyConfiguration<TModel> where TModel : BaseAppModel
    {
        public BaseAppViewConfigurations(TModel model) : base(model)
        {
        }

        public override void ConfigureModel()
        {
            ConfigurePaymentMethod();
        }

        public void ConfigurePaymentMethod()
        {
            ConfigureModel(model => model.PaymentMethod.AccountNumber)
                .Name("Account Number")
                .Type("label");

            ConfigureModel(model => model.PaymentMethod.PaymentCurrency)
                .Name("Payment Currency")
                .Type("label");

            ConfigureModel(model => model.PaymentMethod.Amount)
                .Name("Payment Amount")
                .Type("textbox")
                .Required(true);

            ConfigureModel(model => model.PaymentMethod.AccountName)
                .Name("Account Name")
                .Type("label");

            ConfigureModel(model => model.PaymentMethod.PaymentMethod)
                .Name("Payment Method")
                .Type("label");
        }
    }
}