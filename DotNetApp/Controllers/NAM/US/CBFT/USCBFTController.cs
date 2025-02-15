using Application.Controllers.Base;
using Application.ViewModels.NAM.US.CBFT;

namespace DotNetApp.Controllers.NAM.US.CBFT
{
    public class USCBFTController : BaseController<USCBFTModel>
    {
        internal override string ViewName => "USCBFTView";
    }
}
