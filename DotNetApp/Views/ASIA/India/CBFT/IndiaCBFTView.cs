using Application.ViewModels.ASIA.India.CBFT;
using DotNetApp.Core.Configuration;
using DotNetApp.Core.ViewConfiguration;
using DotNetApp.ViewConfigurations.ASIA.India.CBFT;

namespace Application.Views.ASIA.India.CBFT
{
    public class IndiaCBFTView : BaseView<IndiaCBFTModel>
    {
        public override PropertyConfiguration<IndiaCBFTModel> InvokeConfiguration(IndiaCBFTModel model)
        {
            var configurations = new IndiaCBFTConfiguration(model);
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
