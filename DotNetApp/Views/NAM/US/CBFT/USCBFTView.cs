using Application.ViewModels.NAM.US.CBFT;
using DotNetApp.Core.Configuration;
using DotNetApp.Core.ViewConfiguration;
using DotNetApp.ViewConfigurations.NAM.US.CBFT;

namespace DotNetApp.Views.NAM.US.CBFT
{
  public class USCBFTView : BaseView<USCBFTModel>
    {
        public override PropertyConfiguration<USCBFTModel> InvokeConfiguration(USCBFTModel model)
        {
            var configurations = new USCBFTConfiguration(model);
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
