using Application.Controllers.Base;
using Application.ViewModels.NAM.US.BKT;

namespace DotNetApp.Controllers.NAM.US.BKT
{
    public class USBKTController : BaseController<USBKTModel>
    {
        internal override string ViewName => "USBKTView";
    }
}