using Application.Controllers.Base;
using Application.ViewModels.LandingPage;
using System.Web.Mvc;

namespace Application.Controllers
{
    public class LandingPageController : BaseController<LandingPagModel>
    {
        internal override string ViewName => "LandingPageView";
    }
}