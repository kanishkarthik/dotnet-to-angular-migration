using DotNetApp.Core.Configuration;
using Models = Application.ViewModels.LandingPage;

namespace DotNetApp.ViewConfigurations.LandingPage
{
    public class LandingPageConfiguration : PropertyConfiguration<Models.LandingPagModel>
    {
        public LandingPageConfiguration(Models.LandingPagModel model) : base(model)
        {
        }

        public override void ConfigureModel()
        {
            ConfigureModel(model => model.AccountNumber)
                .Type("lookup")
                .Name("Account Number")
                .Required(true);

            ConfigureModel(model => model.PaymentMethod)
                .Type("dropdown")
                .Name("Payment Method")
                .Required(true);
        }
    }
}