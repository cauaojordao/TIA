using Microsoft.AspNetCore.Identity;
using TIA.Domain.Entities;

namespace TIA.Application.Interfaces
{
    public interface IIdentityService
    {
        Task<IdentityResult> CreateUserAsync(Account domainUser, string password);
        Task<Account?> GetUserByEmailAsync(string email);
    }
}
