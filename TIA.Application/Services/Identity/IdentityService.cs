
using Microsoft.AspNetCore.Identity;
using TIA.Application.Interfaces;
using TIA.Domain.Entities;

namespace TIA.Persistence.Identity
{
    public class IdentityService : IIdentityService
    {
        private readonly UserManager<IdentityUserExtended> _userManager;
        private readonly RoleManager<IdentityRole> _roleManager;

        public IdentityService(UserManager<IdentityUserExtended> userManager, RoleManager<IdentityRole> roleManager)
        {
            _userManager = userManager;
            _roleManager = roleManager;
        }

        public async Task<IdentityResult> CreateUserAsync(Account domainUser, string password)
        {
            var identityUser = new IdentityUserExtended
            {
                UserName = domainUser.Username,
                Email = domainUser.UserEmail,
                Role = domainUser.UserRole
            };

            var result = await _userManager.CreateAsync(identityUser, password);
            if (result.Succeeded)
            {
                await _userManager.AddToRoleAsync(identityUser, domainUser.UserRole);
            }

            return result;
        }

        public async Task<Account?> GetUserByEmailAsync(string email)
        {
            var identityUser = await _userManager.FindByEmailAsync(email);
            if (identityUser == null) return null;

            return new Account
            {
                Id = Guid.Parse(identityUser.Id),
                Username = identityUser.UserName!,
                UserEmail = identityUser.Email!,
                UserRole = identityUser.Role
            };
        }

    }

}
