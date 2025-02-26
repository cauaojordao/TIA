using Microsoft.AspNetCore.Identity;

namespace TIA.Persistence.Identity
{
    public class IdentityUserExtended : IdentityUser
    {
        public string Role { get; set; } = string.Empty;
    }
}
