using TIA.Domain.Entities;

namespace TIA.Domain.Interfaces
{
    public interface IUserRepository : IBaseRepository<Account>
    {
        Task<Account> GetByEmail(string email, CancellationToken cancellationToken);
    }
}
