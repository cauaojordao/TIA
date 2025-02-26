using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using TIA.Domain.Entities;

namespace TIA.Persistence.Context
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        { }

        public DbSet<Account> Users { get; set; }
        public DbSet<AppFile> AppFiles { get; set; }
        public DbSet<Question> Questions { get; set; }
        public DbSet<Answear> Answears { get; set; }

    }
}
