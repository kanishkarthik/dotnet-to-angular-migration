using Application.ViewModels.ASIA.India.DFT;
using DotNetApp.Core.Configuration;
using DotNetApp.Core.ViewConfiguration;
using DotNetApp.ViewConfigurations.ASIA.India.DFT;

namespace Application.Views.ASIA.India.DFT
{
    public class IndiaDFTView : BaseView<IndiaDFTModel>
    {
        public override PropertyConfiguration<IndiaDFTModel> InvokeConfiguration(IndiaDFTModel model)
        {
            var configurations = new IndiaDFTConfiguration(model);
            configurations.ConfigureModel();

            return configurations;
        }

        public override string ConfigreStyles()
        {
            return "<link rel='stylesheet' href='Content/Initiation/Initiation.css'>";
        }

        public override string ConfigureScripts()
        {
            return "<script src='Scripts/Initiation/Initiation.js'/></script>";
        }

        public override string ConfigureFooterPanel()
        {
            return $"<div class='actions'> <button class='primary'>Submit</button><button class='secondary'>Cancel</button></div>";
        }
    }
}
