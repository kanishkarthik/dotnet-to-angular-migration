using System;
using System.Web.Mvc;

namespace Application.Controllers.Base
{
    public abstract class BaseController<TModel> : Controller where TModel : class
    {
        internal abstract string ViewName { get; }

        public virtual ActionResult Index()
        {
            TModel model = Activator.CreateInstance<TModel>();
            return View(ViewName, model);

        }
    }
}